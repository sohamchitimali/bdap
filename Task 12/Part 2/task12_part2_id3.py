# -*- coding: utf-8 -*-
# task12_part2_id3.py
# Simple ID3 Decision Tree Example (Play Tennis dataset)
# Compatible with Python 2.6 (no Counter used)

import csv
import math

# Simple replacement for Counter
def count_values(values):
    freq = {}
    for v in values:
        freq[v] = freq.get(v, 0) + 1
    return freq

# ------------------------------
# Step 1: Load dataset
# ------------------------------
def load_dataset(filename):
    dataset = []
    with open(filename, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)  # first row is header
        for row in reader:
            dataset.append(dict(zip(headers, row)))
    return dataset, headers

# ------------------------------
# Step 2: Entropy calculation
# ------------------------------
def entropy(rows, target_attr):
    values = [row[target_attr] for row in rows]
    freq = count_values(values)
    total = len(values)
    ent = 0.0
    for f in freq.values():
        p = float(f) / total
        ent -= p * math.log(p, 2)
    return ent

# ------------------------------
# Step 3: Information gain
# ------------------------------
def info_gain(rows, attr, target_attr):
    total_entropy = entropy(rows, target_attr)
    values = set(row[attr] for row in rows)
    weighted_entropy = 0.0
    for v in values:
        subset = [row for row in rows if row[attr] == v]
        weighted_entropy += (len(subset) / len(rows)) * entropy(subset, target_attr)
    return total_entropy - weighted_entropy

# ------------------------------
# Step 4: Build tree recursively
# ------------------------------
def id3(rows, attrs, target_attr):
    values = [row[target_attr] for row in rows]
    if values.count(values[0]) == len(values):
        return values[0]  # all same
    if not attrs:
        freq = count_values(values)
        return max(freq, key=freq.get)  # majority vote

    # Choose best attribute
    gains = [(attr, info_gain(rows, attr, target_attr)) for attr in attrs]
    best_attr = max(gains, key=lambda x: x[1])[0]
    tree = {best_attr: {}}

    for v in set(row[best_attr] for row in rows):
        subset = [row for row in rows if row[best_attr] == v]
        new_attrs = [a for a in attrs if a != best_attr]
        tree[best_attr][v] = id3(subset, new_attrs, target_attr)

    return tree

# ------------------------------
# Step 5: Prediction function
# ------------------------------
def classify(tree, sample):
    if not isinstance(tree, dict):
        return tree
    attr = list(tree.keys())[0]
    if sample[attr] in tree[attr]:
        return classify(tree[attr][sample[attr]], sample)
    else:
        return "Unknown"

# ------------------------------
# Main
# ------------------------------
if __name__ == "__main__":
    dataset, headers = load_dataset("/home/cloudera/play_tennis.csv")
    target_attr = "Play"
    attrs = [a for a in headers if a != target_attr]

    print("Building ID3 Decision Tree...")
    tree = id3(dataset, attrs, target_attr)
    print("Decision Tree:", tree)

    # Test with a new sample
    sample = {"Outlook": "Sunny", "Temperature": "Cool", "Humidity": "High", "Wind": "Weak"}
    prediction = classify(tree, sample)
    print("New Sample:", sample)
    print("Predicted Class:", prediction)
