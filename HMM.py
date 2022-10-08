#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: 徐聪
# datetime: 2022-10-08 10:27
# software: PyCharm

import re
import pypinyin
import numpy as np


class HMM(object):

    def __init__(self):
        """
        初始化函数
        """
        self.pi = {}  # 初始状态概率 {word:pro, ..}
        self.A = {}  # 状态转移概率   {phrase:pro, ..}
        self.B = {}  # 观测状态概率 {pinyin:{word:pro, ..}, ..}
        self.dic = {}  # 拼音字典 {pinyin: wordwordword}

    def get_dic(self, dic_path):
        """
        获取拼音字典
        :param dic_path:
        :return:
        """
        f = open(dic_path, encoding='utf-8')
        for line in f.readlines():
            line = re.sub(r'[\ufeff]', '', line).strip().split()
            self.dic[line[0]] = line[1]
        f.close()

    def train_A_B_pi(self, data_path):
        """
        状态转移概率、状态转移概率、观测状态概率
        :return:
        """
        # 统计单字、词组频数
        sw = {}
        dw = {}
        f = open(data_path, encoding='utf-8')

        num_word = 0
        # cnt = 0
        for line in f.readlines():
            # ==============test================
            # cnt += 1
            # if cnt == 10000:
            #     break

            line = re.findall('[\u4e00-\u9fa5]+', line)
            for sentence in line:
                pw = ""
                for word in sentence:
                    # 统计单字
                    if word not in sw:
                        sw[word] = 1
                    else:
                        sw[word] += 1

                    # 统计词组
                    if pw != "":
                        if pw + word not in dw:
                            dw[pw + word] = 1
                        else:
                            dw[pw + word] += 1
                    pw = word
                num_word += 1

        # 统计初始状态概率
        # self.pi # 初始状态概率 {word:pro, ..}
        for word in sw.keys():
            self.pi[word] = sw[word] / num_word

        # 统计状态转移频数
        # self.A # 状态转移概率   {phrase:pro, ..}
        for phrase in dw:
            self.A[phrase] = dw[phrase] / sw[phrase[0]]

        # 计算观测状态频数
        # self.B 观测状态概率 {pinyin:{word:pro, ..}, ..}
        for word in sw:
            # lazy_pinyin 去除拼音平仄
            pinyin = pypinyin.lazy_pinyin(word)[0]
            if pinyin not in self.B.keys():
                self.B[pinyin] = {word: sw[word]}
            else:
                self.B[pinyin][word] = sw[word]

        # 计算观测状态频率
        for pinyin in self.B.keys():
            sum_word = sum(self.B[pinyin].values())
            for word in self.B[pinyin]:
                self.B[pinyin][word] = self.B[pinyin][word] / sum_word

    def predict_pinyin2chinese(self, pinyin):
        """
        根据拼音预测中文句子
        :param pinyin: 拼音字符串，中间用空格分割
        :return:
        """

        # 将拼音转换成列表
        pinyin_list = pinyin.lower().strip().split()

        # 获取各拼音对应的所有汉字
        word_list = []
        for py in pinyin_list:
            if py in self.dic:
                words = re.findall('[\u4e00-\u9fa5]+', self.dic[py])[0]
                word_list.append([word for word in words])

        # 建立id到汉字的映射
        id2word = {}
        word2id = {}
        idx = 0
        for words in word_list:
            for word in words:
                id2word[idx] = word
                word2id[word] = idx
                idx += 1

        # word列表转换成对应的id列表
        word_id_list = [None] * len(word_list)
        for i in range(len(word_list)):
            word_id_list[i] = [None] * len(word_list[i])
            for j in range(len(word_list[i])):
                word_id_list[i][j] = word2id[word_list[i][j]]

        # 利用viterbi算法获取中文句子
        words = self.viterbi(word_id_list, pinyin_list, len(id2word), id2word)
        return "".join(words)

    def viterbi(self, word_id_list, pinyin_list, n, id2word):
        """
        维特比算法求解最大路劲问题
        :param word_id_list: 每个拼音对应的汉字id
        :param pinyin_list: 拼音列表
        :param n: 拼音对应所有汉字的数量之和
        :param id2word: id到汉字的映射
        :return: 中文汉字列表
        """

        cnt = len(word_id_list)  # 拼音数量
        dp = np.zeros((cnt, n))  # dp表
        pre_path = np.zeros((cnt, n), dtype='i4')  # 回溯表

        # 初始化第一个拼音各汉字概率
        for wi in word_id_list[0]:
            if id2word[wi] not in self.pi:
                dp[0][wi] = 0
            else:
                dp[0][wi] = self.pi[id2word[wi]]

        # 归一化处理
        sum_pro = sum(dp[0])
        for wi in word_id_list[0]:
            dp[0][wi] = dp[0][wi] / sum_pro

        # 动态规划计算最大路径
        for i in range(1, cnt):
            wil = word_id_list[i]
            pre_wil = word_id_list[i - 1]
            for wi in wil:
                # 记录最大的概率以及对应id
                max_pro = 0
                max_idx = 0
                for pwi in pre_wil:
                    phrase = id2word[pwi] + id2word[wi]
                    if phrase not in self.A:
                        continue

                    if self.A[phrase] * dp[i - 1][pwi] >= max_pro:
                        max_pro = self.A[phrase] * dp[i - 1][pwi]
                        max_idx = pwi

                if pinyin_list[i] not in self.B or id2word[wi] not in self.B[pinyin_list[i]]:
                    dp[i][wi] = 0
                else:
                    dp[i][wi] = max_pro * self.B[pinyin_list[i]][id2word[wi]]

                # 记录当前最大路径的前一个节点
                pre_path[i][wi] = max_idx

            # 归一化处理 防止数值太小
            sum_pro = sum(dp[i])
            for wi in word_id_list[i]:
                dp[i][wi] = dp[i][wi] / sum_pro

        # 回溯找最优路径
        idx = cnt - 1
        pre = np.argmax(dp[idx])
        word_path = [pre]
        while idx > 0:
            word_path.append(pre_path[idx][pre])
            pre = pre_path[idx][pre]
            idx -= 1
        word_path.reverse()

        # 将id转换成汉字
        words = [None] * len(word_path)
        for i in range(len(word_path)):
            words[i] = id2word[word_path[i]]

        return words