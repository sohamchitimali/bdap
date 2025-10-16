# -*- coding: utf-8 -*-
# task14_hive_bridge.py
# Spark reads HBase table through Hive external table (via HBaseStorageHandler)

from pyspark import SparkContext
from pyspark.sql import HiveContext

# Step 1: Start SparkContext and HiveContext
sc = SparkContext(appName="Task14_Hive_Bridge")
hive = HiveContext(sc)

# Step 2: Use the default Hive database
hive.sql("USE default")

# Step 3: Query the Hive external table (which points to HBase 'employees')
print("=== Data from HBase through Hive ===")
df = hive.sql("SELECT * FROM employeesnew")
df.show()

# Step 4: Simple analytics — count employees by department
print("=== Employees per Department ===")
hive.sql("""
  SELECT dept, COUNT(*) AS cnt
  FROM employeesnew
  GROUP BY dept
  ORDER BY cnt DESC
""").show()

sc.stop()