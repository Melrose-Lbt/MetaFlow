"""
    Copyright © 2022 Melrose-Lbt
    All rights reserved

    Filename: linear regression demo.py
    Description: This demo shows how to use metaflow to handle
        linear regression problems.

    Created by Melrose-Lbt 2022-5-19
"""
import numpy as np
from metalearn import LinearRegression, NormalEquation
from sklearn import linear_model
import matplotlib.pyplot as plt
models = linear_model.LinearRegression()


data_path = './linear_regression_data/ex1data2.txt'


def data_loader(path):
    dataset = []
    with open(path, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n').split(',')
            line[0] = float(line[0])
            line[1] = float(line[1])
            line[2] = float(line[2])
            dataset.append(line)

    return np.array(dataset)


dataset = data_loader(data_path)
# normal equation
equation = NormalEquation(dataset)
# linear regression
model = LinearRegression(dataset, lr=0.00001, normalization=True)
model.train(20000)
model.get_model_info()

# predict
#xx = [[5.1]]
xs = [[2104, 3], [4478, 5], [852, 2]]
x = [[2104, 3], [4478, 5], [852, 2]]
ys = equation.predict(xs)
y = model.predict(x)
print(ys)
print(y)
