"""
SparkSQL practice.

Created: 2024-10-31
Updated: 2024-10-31
"""

from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SparkSQL").getOrCreate()
print(spark)
employees = spark.read.csv("random_data.csv", header=True, inferSchema=True)
print(employees)
employees.printSchema()
print("count:", employees.count())
employees.show(5)
employees.groupby("department").count().show()
employees.groupby("department").agg({"salary": "avg"}).show()

projects = spark.read.json("projects.json", multiLine=True)
projects.show()
projects.printSchema()

merged = projects.join(employees, projects.project_owner == employees.name, "inner")
merged.select(projects.project_name, employees.department).show()
