#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

# import copy
import numpy as np
from scipy.sparse import csc_matrix


class NeighboorMatrix(object):
    def __init__(self, data):
        self.update_neighboor_matrix(data)
        self.dtype = data.dtype

    def update_neighboor_matrix(self, data):
        self.neighboor_matrix = neighboor_matrix(data)

    def get(self, intensity0, intensity1):
        return self.neighboor_matrix[intensity0][intensity1]

    def to_ndarray(self):
        keys = self.keys()
        inv_keys = self.inv_keys()
        sz = len(self.neighboor_matrix)
        ndnghb = np.zeros([sz, sz], dtype=self.dtype)
        for keyx in self.neighboor_matrix:
            nghbx = self.neighboor_matrix[keyx]
            for keyy in nghbx:
                value = nghbx[keyy]
                ndnghb[inv_keys[keyx], inv_keys[keyy]] = value
        return ndnghb

    def keys(self):
        return self.neighboor_matrix.keys()

    def inv_keys(self):
        keys = list(self.keys())
        ii = list(range(len(keys)))
        return dict(zip(keys, ii))


def neighboor_matrix(data):
    csc_matrix((3, 4), dtype=np.int8).toarray()

    nbm = {}
    it = np.nditer(data, flags=['multi_index'])
    while not it.finished:
        mindex0 = it.multi_index
        # print("%d <%s>" % (it[0], mindex0), end=' ')
        data_value0 = data[mindex0]
        for axn in range(len(mindex0)):
            mindex1 = list(mindex0)
            mindex1[axn] = mindex1[axn] + 1
            mindex1 = tuple(mindex1)
            if np.all(np.asarray(mindex1) < np.asarray(data.shape)):
                data_value1 = data[mindex1]
                # budeme vyplnovat jen spodni
                # if data_value0 < data_value1:
                #     data_value0s = data_value0
                #     data_value1s = data_value1
                # else:
                #     data_value0s = data_value1
                #     data_value1s = data_value0
                data_value0s = data_value0
                data_value1s = data_value1

                if data_value0s not in nbm.keys():
                    nbm[data_value0s] = {}
                if data_value1s not in nbm[data_value0s].keys():
                    nbm[data_value0s][data_value1s] = 0
                nbm[data_value0s][data_value1s] += 1

                if data_value1s not in nbm.keys():
                    nbm[data_value1s] = {}
                if data_value0s not in nbm[data_value1s].keys():
                    nbm[data_value1s][data_value0s] = 0

                # if data_value0s != data_value1s:
                #     # we dont want to put the numer into diagonal for twice
                # on diagonal there will be doubled values
                nbm[data_value1s][data_value0s] += 1

        it.iternext()
    return nbm
