# -*- coding: utf-8 -*-
# task12_part1_lr_rdd.py
# Linear Regression with Spark MLlib (RDD API, Spark 1.6)

from pyspark import SparkContext
from pyspark.mllib.regression import LabeledPoint, LinearRegressionWithSGD

# Step 1: Start SparkContext
sc = SparkContext(appName="Task12_Part1_LinearRegression")

# Step 2: Load CSV data (local file)
data = sc.textFile("file:///home/cloudera/housing.csv")

# Step 3: Parse CSV into LabeledPoint (label = price, feature = size)
parsed = data.map(lambda line: line.split(",")) \
             .map(lambda parts: LabeledPoint(float(parts[1]), [float(parts[0])]))

# Step 4: Train Linear Regression model using Stochastic Gradient Descent
model = LinearRegressionWithSGD.train(parsed, iterations=100, step=0.0000001)

# Step 5: Print model parameters
print("Intercept (base price):", model.intercept)
print("Weight (price per sq ft):", model.weights)

# Step 6: Test predictions
print("=== Predictions ===")
for size in [1200, 1800, 2500]:
    predicted_price = model.predict([size])
    print("House size:", size, "sq ft -> Predicted price:", predicted_price)

sc.stop()
