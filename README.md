# Installation

~~~bash
conda create -n ircot python=3.8.0 -y && conda activate ircot
pip install -r requirements.txt
python -m spacy download en_core_web_sm
~~~

# Prepare Data

执行以下命令获取已处理数据：

~~~bash
./download/processed_data.sh
~~~

数据会被下载到`processed_data/{dataset_name}/`

如果您想构建elasticsearch索引并运行retriever或ODQA系统，你还需要下载`raw_data`

~~~bash
./download/raw_data.sh
~~~

# Prepare Prompts

所有可用的prompts都在`prompts/`目录中

# Prepare Retriever and LLM Servers

首先，安装Elasticsearch 7.10

### Install on Linux

~~~bash
# source: https://www.elastic.co/guide/en/elasticsearch/reference/8.1/targz.html
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.10.2-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.10.2-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-7.10.2-linux-x86_64.tar.gz.sha512
tar -xzf elasticsearch-7.10.2-linux-x86_64.tar.gz
cd elasticsearch-7.10.2/
./bin/elasticsearch # start the server
pkill -f elasticsearch # to stop the server
~~~

在9200端口（默认）开启elasticsearch服务，并启动retriever服务器

~~~bash
uvicorn serve:app --port 8000 --app-dir retriever_server
~~~

接下来，对数据集的维基百科语料库进行索引。此步骤需确保`raw_data` 与 `processed_data`已下载

~~~bash
python retriever_server/build_index.py {dataset_name} # hotpotqa, 2wikimultihopqa
~~~

执行上述命令后可得到2个索引文件，名为 `{dataset}-wikipedia`，其数据量分别为：HotpotQA (5,233,329), 2WikiMultihopQA (430,225)

最后，启动LLM服务器：
如果使用flan-t5-*模型，运行如下命令：

~~~bash
MODEL_NAME={model_name} uvicorn serve:app --port 8010 --app-dir llm_server # model_name: flan-t5-xxl, flan-t5-xl, flan-t5-large, flan-t5-base
~~~

如果使用openai模型(codex)，则无需执行上述命令，只需在commaqa/models/gpt3generator.py中第180行填写`OPENAI_API_KEY`即可

# Run Retrieval and ODQA Systems

首先，设置变量：

```bash
- SYSTEM: choose from (`ircot`, `ircot_qa`, `oner`, `oner_qa`, `nor_qa`)
- MODEL: choose from (`codex`, `flan-t5-xxl`, `flan-t5-xl`, `flan-t5-large`, `flan-t5-base`, `none`)
- DATASET: choose from (`hotpotqa`, `2wikimultihopqa`, `musique`, `iirc`)
```

以`_qa`结尾的系统用于ODQA，其他系统用于检索

最终，通过如下命令运行系统：

~~~bash
./reproduce.sh $SYSTEM $MODEL $DATASET
~~~

如果您希望拥有更多的控制权，也可以按以下步骤逐步运行：

~~~bash
# Instantiate experiment configs with different HPs and write them in files.
python runner.py $SYSTEM $MODEL $DATASET write --prompt_set 1
python runner.py $SYSTEM $MODEL $DATASET write --prompt_set 2
python runner.py $SYSTEM $MODEL $DATASET write --prompt_set 3
## if you make a change to base_configs, the above steps need to be rerun to
## regenerate instantiated experiment configs (with HPs populated)

# Run experiments for different HPs on dev set
python runner.py $SYSTEM $MODEL $DATASET predict --prompt_set 1
## predict command runs evaluation at the end by default. If you want to run evaluation
## separately after prediction, you can replace predict with evaluate here.

# Show results for experiments with different HPs
python runner.py $SYSTEM $MODEL $DATASET summarize --prompt_set 1
## Not necessary as such, it'll just show you the results using different HPs in a nice table.

# Pick the best HP and save the config with that HP.
python runner.py $SYSTEM $MODEL $DATASET write --prompt_set 1 --best
python runner.py $SYSTEM $MODEL $DATASET write --prompt_set 2 --best
python runner.py $SYSTEM $MODEL $DATASET write --prompt_set 3 --best

# Run the experiment with best HP on test set
python runner.py $SYSTEM $MODEL $DATASET predict --prompt_set 1 --best --eval_test --official
python runner.py $SYSTEM $MODEL $DATASET predict --prompt_set 2 --best --eval_test --official
python runner.py $SYSTEM $MODEL $DATASET predict --prompt_set 3 --best --eval_test --official
## predict command runs evaluation at the end by default. If you want to run evaluation
## separately after prediction, you can replace predict with evaluate here.

# Summarize best test results for individual prompts and aggregate (mean +- std) of them)
python runner.py $SYSTEM $MODEL $DATASET summarize --prompt_set 1 --best --eval_test --official
python runner.py $SYSTEM $MODEL $DATASET summarize --prompt_set 2 --best --eval_test --official
python runner.py $SYSTEM $MODEL $DATASET summarize --prompt_set 3 --best --eval_test --official
python runner.py $SYSTEM $MODEL $DATASET summarize --prompt_set aggregate --best --eval_test --official
## The mean and std in the final command is what we reported in the paper.
~~~
