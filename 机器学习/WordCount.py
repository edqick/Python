# -*- coding:utf-8 -*-
from pyspark import SparkContext
from pyspark import SparkConf
import os


def CreateSparkContext(mode):
    sparkConf = SparkConf().setAppName("WordCounts").setMaster(mode)
    sc = SparkContext(conf=sparkConf)
    print("master=" + sc.master)
    SetLogger(sc)
    SetPath(sc)
    return sc


def SetLogger(sc):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org").setLevel(logger.Level.ERROR)
    logger.LogManager.getLogger("akka").setLevel(logger.Level.ERROR)
    logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)


def SetPath(sc):
    global Path
    if sc.master[0:5] == "local":
        Path = "file:/d:/spark/"
    else:
        Path = "hdfs://localhost:9000/spark/input/"


if __name__ == '__main__':
    print("开始执行 RunWordCount")
    sc = CreateSparkContext("local")
    print("开始读取文本文件...")
    textFile = sc.textFile(Path+"input/test.txt")
    print("文本文件共 " + str(textFile.count()) + " 行 ")
    countRDD = textFile.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(
        lambda x, y: x + y)
    print("文字统计共 " + str(countRDD.count()) + " 项数据 ")
    print("开始保存至文本文件...")
    try:
        countRDD.saveAsTextFile(Path+"output/wordcount1")
    except Exception as e:
        print("输出目录已经存在，请先删除原有目录。")
        sc.stop()