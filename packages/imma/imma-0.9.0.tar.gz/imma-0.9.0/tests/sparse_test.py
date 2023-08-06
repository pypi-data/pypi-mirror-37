#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)
# import funkcí z jiného adresáře
import os.path

import unittest

import numpy as np
import os

# import io3d
import io3d.datasets
import imma.sparse as ima


class ImageManipulationTest(unittest.TestCase):
    interactivetTest = False

    # interactivetTest = True

    def test_store_to_SparseMatrix_and_back(self):
        data = np.zeros([4, 4, 4])
        data = np.zeros([4, 4, 4])
        data[1, 0, 3] = 1
        data[2, 1, 2] = 1
        data[0, 1, 3] = 2
        data[1, 2, 0] = 1
        data[2, 1, 1] = 3

        dataSM = ima.SparseMatrix(data)
        self.assertTrue(ima.isSparseMatrix(dataSM), "Check sparse matrix")

        data2 = dataSM.todense()
        self.assertTrue(np.all(data == data2))


if __name__ == "__main__":
    unittest.main()
