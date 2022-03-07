"""
    Copyright © 2022 Melrose-Lbt
    All rights reserved

    Filename: _Module.py
    Description: This file provide root class for models.

    Created by Melrose-Lbt 2022-3-5
"""
import abc
from collections import OrderedDict
from ._Tensor_core import Tensor


class Modules:

    def __init__(self, core_module=False):
        """
            If core_module is True, that means this class is a layers module defined by developers
            If core_module is False, that means this class is a user defined model
        """
        self.core_module = core_module
        # Get model's parameters
        self._parameters = OrderedDict()

    def __call__(self, x):
        """
            Call forward function and return.
        :param x: Tensor input
        :return: self.forward(x)
        """
        return self.forward(x)

    def __setattr__(self, key, value):
        """
            Record model's trainable parameters into self._parameters: -> dict
        """
        if isinstance(value, OrderedDict):
            if self.core_module:
                pass
            else:
                self.__dict__[key] = value
                # counter makes sure that self._parameters record different value
                module_layer_cnt = 0
                for layers in self.__dict__:
                    module_layer_cnt += 1

                    if isinstance(self.__dict__[layers], bool):
                        continue
                    else:
                        layers_dict = self.__dict__[layers].__dict__
                        for params_name in layers_dict:
                            if isinstance(layers_dict[params_name], Tensor):
                                if layers_dict[params_name].grad_require:
                                    self._parameters[params_name + str(module_layer_cnt)] = layers_dict[params_name]
                                else:
                                    continue
                            else:
                                continue

                if len(self._parameters) == 0:
                    raise AttributeError("cannot assign parameters after Modules.__init__() call")
        else:
            self.__dict__[key] = value

    def layers_filter(self):
        """
            A generator.
            Get models layer's name and its value. Get rid of those objects who are not
        belong to Modules. Only if self.core_modules is False that this function could
        be called.
        """
        for name in self.__dict__:
            if isinstance(self.__dict__[name], Modules):
                yield name, self.__dict__[name]
            else:
                continue

    def get_model_info(self):
        if self.core_module:
            raise AttributeError("this module is core module, you could only use this method when your model is "
                                 "defined by yourself.")
        for name, layers in self.layers_filter():
            print('-' * 50)
            print(">>> Layer name:{} ".format(name))
            print('')
            layers.get_module_info()
            print('-' * 50)

    @abc.abstractmethod
    def get_module_info(self):
        """
            For developers,You have to rewrite this method when you create a new module.
            This method is layer-wise information, it could be called by 'get_model_info'
        method.
        """

    def get_parameters(self):
        """
            A generator.
            Get key word from 'self._parameters: OrderedDict()', and return its
        key word and value.
        """
        for items in self._parameters:
            yield items, self._parameters[items]

    def parameters(self):
        """
            Get models trainable parameters.
        :return: Model params dict
        """
        for name, params in self.get_parameters():
            yield name, params

    @abc.abstractmethod
    def forward(self, x):
        """
            Here you need to define your model's compute process.
        :param x: Tensor input
        :return: Tensor output
        """
