"""
    Copyright © 2022 Melrose-Lbt
    All rights reserved

    Filename: cluster.py
    Description: This file provide multiple clustering algorithm.

    Created by Melrose-Lbt 2022-3-7
"""
import random
import numpy as np
from scipy.cluster.hierarchy import dendrogram
from utils import euclidean_distance, find_min_dis
import matplotlib.pyplot as plt


class Kmeans:
    """
        K-means algorithm.
    """
    def __init__(self, dataset, k):
        if isinstance(dataset, list):
            self.dataset = dataset
        else:
            raise ValueError("argument dataset has to be list data type!")
        self.k = k
        self.cluster_center = self.random_choose()
        self.dot_set = [[] for i in range(self.k)]
        self.last_cluster_center = []

        # self.last_dot_set = [[] for i in range(self.k)]

    def init_cluster(self):
        """
            Initialize dot set.
        :return:
        """
        for i in range(self.k):
            self.dot_set[i].append(self.cluster_center[i])

    def random_choose(self):
        """
            Choose random dots as initial dots from dataset.
        :return:
        """
        cluster_center = []
        cluster_index = random.sample(range(0, len(self.dataset)), self.k)
        for i in range(self.k):
            cluster_center.append(self.dataset[cluster_index[i]])

        return cluster_center

    def center_stable(self):
        """
            Judge center point is stable or not.
        :return: bool value
        """
        if self.cluster_center == self.last_cluster_center:
            return False
        return True

    def check_dot_exist(self, dot):
        """
            Called by refresh_dot_set function. Check if this dot exists in
        current dot set.
        :param dot: a single dot
        :return: bool, index
        """
        for cluster_index in range(self.k):
            if dot in self.dot_set[cluster_index]:
                return True, cluster_index
        return False, -1

    def refresh_dot_set(self, min_index, dot):
        """
            Refresh dot set to the renewed one.
        :param min_index: minimum distance index
        :param dot: a single dot
        """
        bool_value, cluster_index = self.check_dot_exist(dot)
        if bool_value:
            if cluster_index == min_index:
                pass
            else:
                self.dot_set[cluster_index].remove(dot)
                self.dot_set[min_index].append(dot)
        else:
            self.dot_set[min_index].append(dot)

    def compute_centers(self):
        """
            Compute cluster's center value.
        """
        self.cluster_center = []
        for cluster_index in range(self.k):
            new_center = np.mean(np.array(self.dot_set[cluster_index]), axis=0)
            self.cluster_center.append(list(new_center))

    def train(self):
        """
            Train logic.
        """
        # Choose k dots as initial cluster centers
        self.init_cluster()

        while self.center_stable():
            self.last_cluster_center = self.cluster_center
            # self.last_dot_set = copy.deepcopy(self.dot_set)
            for items in self.dataset:
                dis_set = []
                for i in range(self.k):
                    dis_set.append(euclidean_distance(items, self.cluster_center[i]))
                min_dis_index = dis_set.index(min(dis_set))
                self.refresh_dot_set(min_dis_index, items)
            self.compute_centers()

        print(self.dot_set)

    def show_img(self):
        color_set = ['blue', 'green', 'yellow', 'gold', 'green']
        for index, clusters in enumerate(self.dot_set):
            x_label, y_label = [], []
            for items in clusters:
                x_label.append(items[0])
                y_label.append(items[1])
            plt.scatter(x_label, y_label, marker='o', color=color_set[index])

        center_x, center_y = [], []
        for i in self.cluster_center:
            center_x.append(i[0])
            center_y.append(i[1])

        plt.scatter(center_x, center_y, marker='x', color='red')
        plt.legend()
        plt.show()


class HierarchicalClustering:
    """
        Hierarchical clustering algorithm.
    """
    def __init__(self, dataset, threshold=1, method='min'):
        """

        :param dataset: dataset
        :param threshold: if you choose k, it'll stop at kth cluster
        :param method: 'min': single linkage
                       'max': complete linkage
                       'average': average linkage
        """
        self.dataset = np.array(dataset)
        self.threshold = threshold
        self.method = method
        self.data_num = np.array(dataset).shape[0]
        self.dot_set = [[] for i in range(self.data_num)]
        self.cluster_id = [i for i in range(len(dataset))]
        self.info_matrix = []

    def init_dot_set(self):
        """
            Set every data point to a single cluster. Bottom up method.
        """
        for i, cluster in enumerate(self.dot_set):
            cluster.append(list(self.dataset[i]))

    def _info_register(self, row_index, col_index, min_dis):
        """
            Register information for 'show_img' method.
        :param row_index: the row which contains minimum distance
        :param col_index: the column which contains minimum distance
        :param min_dis: minimum distance
        """
        info = [self.cluster_id[row_index[0]], self.cluster_id[col_index[0]], min_dis,
                len(self.dot_set[row_index[0]]) + len(self.dot_set[col_index[0]])]
        self.info_matrix.append(info)

    def single_linkage(self):
        """
            Single linkage method. It automatically computes distance matrix for every
        iteration. Then it'll find minimum data location and merge clusters which dis-
        tance is the minimum over all clusters.
            It'll also register its merging process into info matrix. This info matrix
        will use 'dendrogram' method to draw a picture of merging process.
        """
        self.init_dot_set()
        cluster_id_cnt = self.cluster_id[-1]
        while len(self.dot_set) > self.threshold:
            # renew distance matrix
            dis_matrix = np.zeros((len(self.dot_set), len(self.dot_set)))
            for index in range(len(self.dot_set)):
                for sub_index in range(index, len(self.dot_set)):
                    dis_matrix[index][sub_index] = find_min_dis(self.dot_set[index], self.dot_set[sub_index])

            # minimum dot in distance matrix
            row_index, col_index = np.where(dis_matrix == np.min(dis_matrix[np.nonzero(dis_matrix)]))
            min_dis = np.min(dis_matrix[np.nonzero(dis_matrix)])

            del_list = [list(self.dot_set[row_index[0]]), list(self.dot_set[col_index[0]])]
            del_id_list = [row_index[0], col_index[0]]
            # register information
            self._info_register(row_index, col_index, min_dis)
            self.dot_set[row_index[0]] += self.dot_set[col_index[0]]

            self.cluster_id[row_index[0]] = cluster_id_cnt + 1
            cluster_id_cnt += 1

            self.dot_set.remove(del_list[-1])
            self.cluster_id.pop(del_id_list[-1])

        print(self.dot_set)

    def complete_linkage(self):
        pass

    def average_linkage(self):
        pass

    def train(self):
        """
            Train logic.
            Hierarchical clustering has three different types. Although they are
        different, the model underneath the algorithm is actually same. What dif-
        ferentiate them is the way to compute distance between two clusters.
            Train method actually acts as a scheduler. It takes 'self.method' in,
        figures out which way user want to go and call that function accordingly.
        It provides 3 methods.

            'simple': This means when it comes to compute distance between two
        clusters, algorithm will compute minimum distance between them. Based on
        this value, than it will combine these two clusters into single one.

            'complete': This means when it comes to compute distance between two
        clusters, algorithm will compute maximum distance between them.

            'average': This means when it comes to compute distance between two
        clusters, algorithm will compute maximum distance between them.
        """
        if self.method == 'single':
            self.single_linkage()
        elif self.method == 'complete':
            self.complete_linkage()
        elif self.method == 'average':
            self.average_linkage()

    def show_img(self):
        """
            Show images when clustering. Use 'scipy.cluster.hierarchy' package.
        dendrogram method. This method needs formed information matrix as input.

        Information matrix:
            A row:
                A row in information matrix represents for one iteration. The
            number of rows in information matrix are random. It depends on how
            many iterations it'll need to merge into single cluster,

            A column:
                A column has to have four types of information.
                1. id of original cluster a
                2. id of original cluster b
                3. distance between a and b
                4. id of new cluster combined by a and b

        """
        dn = dendrogram(np.array(self.info_matrix))
        plt.show()


if __name__ == "__main__":
    data = [[0, 0], [0, 1], [2, 0], [3, 3], [4, 4]]
    cluster = Kmeans(data, 3)
    #cluster = HierarchicalClustering(data, method='single')
    cluster.train()
    cluster.show_img()
