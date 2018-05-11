# -*- coding: UTF-8 -*-
'''
训练数据：ratings.csv
测试数据：movies.csv
通过机器学习<协同过滤>算法构建推荐模型
'''
from pyspark.mllib.recommendation import ALS,MatrixFactorizationModel
from pyspark import SparkConf, SparkContext

def SetLogger( sc ):
    logger = sc._jvm.org.apache.log4j
    logger.LogManager.getLogger("org"). setLevel( logger.Level.ERROR )
    logger.LogManager.getLogger("akka").setLevel( logger.Level.ERROR )
    logger.LogManager.getRootLogger().setLevel(logger.Level.ERROR)    

def SetPath(sc):
    global Path
    if sc.master[0:5]=="local" :
        Path="file:/d:/spark/"
    else:   
        Path="hdfs://localhost:9000/spark/"
  
def CreateSparkContext(mode):
    sparkConf = SparkConf().setAppName("RecommendTrain").setMaster(mode)
    sc = SparkContext(conf = sparkConf)
    print("master="+sc.master)
    SetLogger(sc)
    SetPath(sc)
    return (sc)
    
  
def PrepareTrainData(sc):
    #----------------------1.建立用户评价数据-------------
    print("开始读取用户评分数据...")
    rawUserData = sc.textFile(Path+"input/ml-latest-small/ratings.csv")
    rawRatings = rawUserData.map(lambda line: line.split(",")[:3])
    head = rawRatings.first()
    rawRatings = rawRatings.filter(lambda line:line!=head)
    ratingsRDD = rawRatings.map(lambda x: (x[0],x[1],x[2]))
    #----------------------2.显示数据项数-------------
    numRatings = ratingsRDD.count()
    numUsers = ratingsRDD.map(lambda x: x[0] ).distinct().count()
    numMovies = ratingsRDD.map(lambda x: x[1]).distinct().count()
    print("共计：ratings: " + str(numRatings) +" User:" + str(numUsers) + " Movie:" +    str(numMovies))
    return(ratingsRDD)

def PrepareTestData(sc):
    print("开始读取电影ID与名称字典...")
    itemRDD = sc.textFile(Path+"input/ml-latest-small/movies.csv")
    movieList= itemRDD.map( lambda line : line.split(",")).map(lambda line:[line[0],line[1]]).collect()
    movieTitle = dict(movieList)
    return(movieTitle)

def SaveModel(sc): 
    try:        
        model.save(sc,Path+"output/ALSmodel")
        print("已存储 Model 在ALSmodel")
    except Exception :
        print("Model已经存在,请先删除再存储.")        

def loadModel(sc):
    try:
        model = MatrixFactorizationModel.load(sc, Path+"output/ALSmodel")
        print("载入ALSModel模型")
    except Exception:
        print("找不到ALSModel模型,请先训练")
    return model

def RecommendMovies(model, movieTitle, inputUserID):
    RecommendMovie = model.recommendProducts(inputUserID, 10)
    print("针对用户id: " + str(inputUserID) + " 推荐下列电影:")
    for rmd in RecommendMovie:
        print("针对用户id: %s 推荐电影: %s 推荐评分: %s"%(rmd[0],movieTitle[str(rmd[1])],rmd[2]))

def RecommendUsers(model, movieTitle, inputMovieID) :
    RecommendUser = model.recommendUsers(inputMovieID, 10)
    print("针对电影id: %s 电影名: %s 推荐下列用户id: "%(inputMovieID,movieTitle[str(inputMovieID)]))
    for rmd in RecommendUser:
        print("针对用户id %s  推荐评分 %s"%(rmd[0],rmd[2]))


if __name__ == "__main__":
    sc=CreateSparkContext("local")
    print("==========准备训练数据===========")
    ratingsRDD = PrepareTrainData(sc)#训练数据
    print("==========训练阶段===============")
    print("开始ALS训练,参数rank=5,iterations=10, lambda=0.1");
    model = ALS.train(ratingsRDD, 5, 10, 0.1)
    # print("========== 存储Model========== ==")
    # SaveModel(sc)
    print("==========准备测试数据===============")
    movieTitle = PrepareTestData(sc)
    print("==========载入模型===============")
    model = loadModel(sc)
    RecommendMovies(model, movieTitle, 1)#为用户1推荐10部电影
    RecommendUsers(model, movieTitle, 858)#为编号为858的电影推荐10个用户

