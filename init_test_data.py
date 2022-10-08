#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: 徐聪
# datetime: 2022-10-08 14:00
# software: PyCharm

import re
import pypinyin

input_path = r"dataset\movie_lines.txt"
output_path = r"dataset\test2.text"

input_file = open(input_path, encoding='utf-8')
output_file = open(output_path, "w", encoding='utf-8')

for line in input_file.readlines():
    sentences = re.findall("[\u4e00-\u9fa5]+", line)
    for sentence in sentences:
        if len(sentence) >= 8:
            output_file.write(" ".join(pypinyin.lazy_pinyin(sentence)) + "\n")
            output_file.write(sentence + "\n")

input_file.close()
output_file.close()
