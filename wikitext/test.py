
from pyspark import SparkContext
sc = SparkContext()
data = [1, 2, 3, 4, 5]
distData = sc.parallelize(data)

