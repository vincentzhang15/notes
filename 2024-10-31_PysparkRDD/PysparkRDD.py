"""
Setup:
- pip install pyspark
- PYSPARK_PYTHON=python env (https://stackoverflow.com/questions/53252181/python-worker-failed-to-connect-back)

Created: 2024-10-31
Updated: 2024-10-31
"""

from pyspark import SparkConf, SparkContext

sc = SparkContext(conf=SparkConf().setAppName("Test").setMaster("local"))
rdd = sc.parallelize(list(range(15)))
print("count:", rdd.count())
print("max:", rdd.max())
print("mean:", rdd.mean())
rdd = rdd.map(lambda x: x+1)
print("x+1:", rdd.collect())
rdd = rdd.filter(lambda x: x%2==0)
print("even:", rdd.collect())
