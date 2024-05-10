# import matplotlib
# import matplotlib.pyplot as plt
# import numpy as np
#
# # 假设有以下准确率数据
# person1 = [0.476, 0.737]
# person2 = [0.408, 0.756]
# person3 = [0.425, 0.799]
# person4 = [0.486, 0.741]
# person5 = [0.451, 0.701]
#
# # 人员名称列表
# people = ['计算机网络', '数据结构', '操作系统', '计算机组成原理', '数据库系统概论']
#
# # 准确率标签列表
# accuracy_labels = ['EM', 'F1']
#
# # 准确率颜色列表
# colors = [(1.0, 0.5, 0.5), (0.5, 1.0, 0.5)]
# # colors = ['pink', 'cyan']
#
# # 初始化条形位置
# index = np.arange(len(people))
#
# # 计算条形宽度
# bar_width = 0.25
#
# # 绘制条形图
# fig, ax = plt.subplots()
# for i, label in enumerate(accuracy_labels):
#     ax.bar(index + i * bar_width, [person[i] for person in [person1, person2, person3, person4, person5]], bar_width,
#            label=label, color=colors[i])
#
# # 计算x轴标签位置，确保它们位于每个人的三个条形的中间位置
# tick_positions = index + (len(accuracy_labels) - 1) * bar_width / 2
#
# # 设置x轴标签和刻度
# ax.set_xticks(tick_positions)
# ax.set_xticklabels(people)
# # 汉字字体，优先使用楷体，找不到则使用黑体
#
# # 设置y轴标签
# #ax.set_ylabel('Accuracy')
# #ax.set_xlabel("人员编号")
# # 汉字字体，优先使用楷体，找不到则使用黑体
# plt.rcParams['font.sans-serif'] = ['SimSun']
# plt.rcParams['font.size'] = 10.5
# plt.xlabel('课程名称')
# plt.ylabel('性能指标')
# #plt.title('IQ直方图：$\mu=100$, $\sigma=15$')
# plt.title('问答系统性能展示图')
#
# # 添加图例
# ax.legend()
#
# # 显示图表
# # plt.tight_layout()
# # plt.show()
#
# # 显示图表
# # plt.tight_layout()
# # plt.show()
# plt.savefig('1.png', dpi=1000)

# file_path = r'C:\Users\DELL\Desktop\requirements.txt'  # 替换为你的文件路径
#
# # 读取文件内容
# with open(file_path, 'r') as file:
#     content = file.read()
#
# # 替换文本中的'='为'=='
# new_content = content.replace('=', '==')
#
# # 将替换后的内容写入文件
# with open(file_path, 'w') as file:
#     file.write(new_content)

import matplotlib.pyplot as plt
import numpy as np

x = np.arange(3)
recall1 = [71.4, 74.7, 78.5]
recall2 = [88.9, 91.1, 92.1]
# 多数据并列柱状图
bar_width = 0.25
tick_label = ['2', '3', '4']
plt.bar(x, recall1, bar_width, align='center', color='#66c2a5', hatch='/', zorder=1, label='HotpotQA')
plt.bar(x+bar_width, recall2, bar_width, align='center', color='#8da0cb', hatch='/', zorder=1, label='2WikiMultihopQA')
plt.xlabel('the Number of Branches in ToT')
plt.ylabel('Retrieval Recall')
plt.xticks(x+bar_width/2, tick_label)
plt.legend(bbox_to_anchor=(0.67, 1), borderaxespad=0.5)
plt.show()
