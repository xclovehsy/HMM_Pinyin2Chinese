#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: 徐聪
# datetime: 2022-10-08 10:28
# software: PyCharm

from HMM import HMM


def cal_accuracy(text, label):
    num_right = 0
    for i in range(len(text)):
        if text[i] == label[i]:
            num_right += 1
    return num_right / len(text)


dic_path = r"dataset\pinyin2hanzi.txt"
toutiao_path = r"dataset\toutiao_cat_data.txt"
test_path = r"dataset\test1.txt"
pinyin_list = []
label_list = []

# 训练HMM模型
hmm = HMM()
hmm.get_dic(dic_path)
hmm.train_A_B_pi(toutiao_path)

# 读取测试文件数据
f = open(test_path, encoding='gbk')
flag = True
for line in f.readlines():
    if flag:
        pinyin_list.append(line.strip('\n').lower())
    else:
        label_list.append(line.strip('\n'))
    flag ^= 1

# 测试模型
acc_sum = 0
for i in range(len(pinyin_list)):
    pre = hmm.predict_pinyin2chinese(pinyin_list[i])
    acc = cal_accuracy(pre, label_list[i])
    acc_sum += acc

    print(f"pinyin={pinyin_list[i]}")
    print(f"predict={pre}")
    print(f"label={label_list[i]}")
    print(f"accuracy={acc}\n")

# 打印总的准确性
print(f"average accuracy = {acc_sum / len(pinyin_list)}")
