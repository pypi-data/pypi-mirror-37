from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession,SQLContext
from pyspark.sql.functions import when, lit, col
from pyspark.sql.types import DateType
from py4j.protocol import Py4JJavaError

from functools import reduce
from pyspark.sql import DataFrame
import pandas
from pyspark.sql.types import DoubleType, FloatType
from pyspark.sql.types import *
from pyspark.sql import SparkSession, SQLContext

import random

class Spark:
  def __init__(self, project= "DEFAULT"):
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    app_name = ""
    for i in range(12):
        app_name = app_name + alphabet[random.randrange(len(alphabet))]
    app_name = "WB_SESSION_"+project+"_"+app_name
    self.spark = SparkSession.builder\
                .appName(app_name)\
                .enableHiveSupport()\
                .config("spark.yarn.executor.memoryOverhead","4G")\
                .config("spark.executor.memory", "12G")\
                .config("spark.dynamicAllocation.enabled", "true")\
                .config("spark.dynamicAllocation.initialExecutors", "2")\
                .config("spark.dynamicAllocation.maxExecutors","5")\
                .config("spark.executor.cores", "8")\
                .config("spark.cores.max", "3")\
                .config("spark.driver.memory", "4G")\
                .config("spark.ui.killEnabled", "true")\
                .getOrCreate()
    
    self.sqlContext = SQLContext(self.spark)
    self.app_name = app_name
    print('Sessão aberta com o nome: '+app_name)
  
  def getSpark(self):
    return self.spark
  
  def getAppName(self):
    return self.app_name
  
  def getSqlContext(self):
    return self.sqlContext
  
  
  def log(self, data):
    sparkcontext = self.spark.sparkContext
    app_id = sparkcontext.applicationId
    
  
  