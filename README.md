# Installation

```bash
conda create -n ircot python=3.8.0 -y && conda activate ircot
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

# Prepare Data

You can download all our processed data by running

```bash
./download/processed_data.sh
```

The data will be downloaded in `processed_data/{dataset_name}/`. 

You'll also need `raw_data` if you want to build elasticsearch indices and run retriever or odqa systems.

```bash
./download/raw_data.sh
```

The data will be downloaded in `raw_data/{dataset_name}/`.

# Prepare Prompts

All our prompts are available in `prompts/` directory. 

# Prepare Retriever and LLM Servers

First, install Elasticsearch 7.10.

### Install on Linux

```bash
# source: https://www.elastic.co/guide/en/elasticsearch/reference/8.1/targz.html
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.10.2-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.10.2-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-7.10.2-linux-x86_64.tar.gz.sha512
tar -xzf elasticsearch-7.10.2-linux-x86_64.tar.gz
cd elasticsearch-7.10.2/
./bin/elasticsearch # start the server
pkill -f elasticsearch # to stop the server
```

Start the elasticsearch server on port 9200 (default), and then start the retriever server as shown here.

```bash
uvicorn serve:app --port 8000 --app-dir retriever_server
```

Next, index the wikipedia corpuses for the datasets. Make sure you've downloaded `raw_data` and `processed_data`.

```bash
python retriever_server/build_index.py {dataset_name} # hotpotqa, 2wikimultihopqa
```

After indexing you can check the number of documents in each index by running `curl localhost:9200/_cat/indices`. You should have 2 indices, one for each dataset, called `{dataset}-wikipedia`. Make sure they match up to the statistics given in the paper. You should expect to see the following sizes: HotpotQA (5,233,329), 2WikiMultihopQA (430,225).

Next, if you want to use flan-t5-* models, start the llm_server by running:

```bash
MODEL_NAME={model_name} uvicorn serve:app --port 8010 --app-dir llm_server # model_name: flan-t5-xxl, flan-t5-xl, flan-t5-large, flan-t5-base
```

If you want to use openai models (e.g., codex in our experiments), you don't need to start it. In that case, you just need to set the environment variable `OPENAI_API_KEY`.

# Prepare BERT-style Evidence Classifier

Before running the entire system, you also need to download the classifier model file (link: https://pan.baidu.com/s/10vBE58S9PbNhP1f3w6NH5g, extracted code: 4hrl) and extract it to the root directory.

# Run Retrieval and ODQA Systems

First, set the variables:

- SYSTEM: choose from (`ircot`, `ircot_qa`, `oner`, `oner_qa`, `nor_qa`)
- MODEL: choose from (`codex`, `flan-t5-xxl`, `flan-t5-xl`, `flan-t5-large`, `flan-t5-base`, `none`)
- DATASET: choose from (`hotpotqa`, `2wikimultihopqa`, `musique`, `iirc`)

The systems ending with `_qa` are for ODQA and others are for retrieval.

Now you can run the system using (language) model and dataset of your choice by running:

```bash
./reproduce.sh $SYSTEM $MODEL $DATASET
```

If you prefer to have more control, you can also run it step-by-step as follows:

```bash
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
```

