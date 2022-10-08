# HMM_Pinyin2Chinese

**HMM 隐马尔可夫模型**

拼音转汉字算法实现

**文件目录树：**

|-- DataSet 数据集
|   |-- movie_lines.txt 经典电影台词
|   |-- pinyin2hanzi.txt 拼音汉字字典
|   |-- test1.txt 测试数据集1
|   |-- test2.txt 测试数据集2
|   -- toutiao_cat_data.txt 头条新闻语料数据，用于训练HMM模型
|-- HMM.py HMM模型类
|-- README.md 
|-- init_test_data.py 初始化
|-- main.py 测试模型准确性

**模型测试结果：**

![image-20221008181909433](https://xc-figure.oss-cn-hangzhou.aliyuncs.com/img/202210081819553.png)

![image-20221008182000936](https://xc-figure.oss-cn-hangzhou.aliyuncs.com/img/202210081820003.png)