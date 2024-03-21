from pyspark.conf import SparkConf
from pyspark.context import SparkContext

def spark_session():
    conf = SparkConf()
    conf.setMaster("mesos://127.0.0.1:5050").setAppName("Miner Jobs")