#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
import numpy as np


class SparseMatrix():
    def __init__(self, ndarray):
        self.coordinates = ndarray.nonzero()
        self.shape = ndarray.shape
        self.values = ndarray[self.coordinates]
        self.dtype = ndarray.dtype
        self.sparse = True

    def todense(self):
        dense = np.zeros(self.shape, dtype=self.dtype)
        dense[self.coordinates[:]] = self.values
        return dense


def isSparseMatrix(obj):
    return obj.__class__.__name__ == 'SparseMatrix'


