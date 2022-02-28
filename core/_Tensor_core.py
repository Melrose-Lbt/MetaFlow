"""
    Copyright © 2022 Melrose-Lbt
    All rights reserved

    Filename: _Tensor_core.py
    Description: This file defines basic and core data structure in MetaFlow
        —— Tensor. Tensor is base class for everything in MetaFlow, for inst
        -ance, neural network layers, data loader, operations and so on.
            Tensor class also provides some class method for simple tensor op
        -eration like add, multiply, matrix multiply and so on.

    Created by Melrose-Lbt 2022-2-28
"""

import numpy as np
import abc
from numpy import ndarray


class Tensor:
    def __init__(self, *args, grad_require=False):
        tensors = []
        self.parents = []
        self.children = []
        for arg in args:
            tensors.append(arg)
        if len(tensors) > 1:
            self.value = self.compute_value(*args).value
        elif len(tensors) == 1:
            self.value = np.array(tensors[0], dtype=float)
        self.shape = self.value.shape
        self.grad = None
        self.grad_require = grad_require
        self.grad_fn = None

    def __str__(self):
        return "<{}, shape={}, dtype=Tensor.float>".format(self.value, self.shape)

    def get_parents(self):
        """
            Get this Tensor's parents list.
        """
        return self.parents

    def get_child(self):
        """
            Get this Tensor's children list.
        """
        return self.children

    def forward(self):
        pass

    def backward(self):
        pass

    @abc.abstractmethod
    def compute_value(self, *args):
        """
            Compute value of a tensor from its parent nodes. And return
        it to self.value. Could be overwritten when necessary.
        :return:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def compute_grad(self):
        """
            Compute gradient based on its children tensors. And return
        it to self.grad. Could be overwritten when necessary.
        :return:
        """
        raise NotImplementedError

    # Tensor-wise OPs
    @classmethod
    def add(cls, tensor1, tensor2):
        """
            Class method for adding operation.
            Examples:
                Tensor.add(a, b)

            :return an instantiated Tensor
        """
        return Tensor(np.add(tensor1.value, tensor2.value))

    @classmethod
    def mul(cls, tensor1, tensor2):
        """
            Element-wise multiply two tensors.
            Examples:
                Tensor.mul(a, b)

            :return an instantiated Tensor
        """
        return Tensor(np.multiply(tensor1.value, tensor2.value))

    @classmethod
    def matmul(cls, tensor1, tensor2):
        """
            Matrix multiply.
            Examples:
                Tensor.matmul(a, b)

            :return an instantiated Tensor
        """
        return Tensor(np.matmul(tensor1.value, tensor2.value))

    @classmethod
    def exp(cls, tensor):
        """
            Exponential operation.
            Examples:
                Tensor.exp(a)

            :return an instantiated Tensor
        """
        return Tensor(np.exp(tensor.value))


class my(Tensor):
    def __init__(self):
        super().__init__()


if __name__ == "__main__":
    a = Tensor([1, 2, 3])
    b = Tensor([2, 2, 2])
    print(Tensor.add(a, b))
