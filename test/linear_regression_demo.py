import numpy as np
from metalearn import LinearRegression
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
x = [[2104, 3], [4478, 5], [852, 2]]
model = LinearRegression(dataset, normalization=True)
model.train(100)
model.get_model_info()
y = model.predict(x)
print(y)