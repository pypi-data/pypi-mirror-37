#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

import unittest
import numpy as np

import imma.measure


class MeasurementTest(unittest.TestCase):

    def test_neigh_matrix(self):
        data = np.zeros((3, 4), dtype=int)
        data[:3, 1] = 1
        data[2:, 2] = 2
        data[0, 1:] = 3

        import imma.measure
        nbm = imma.measure.cooccurrence_matrix(data)
        nbm[1][0]
        self.assertEqual(nbm[1][0], nbm[0][1])
        self.assertEqual(nbm[3][0], nbm[0][3])

    def test_neigh_matrix_obj(self):
        data = np.zeros((3, 4), dtype=int)
        data[:3, 1] = 1
        data[2:, 2] = 2
        data[0, 1:] = 3
        #
        nbm = imma.measure.CooccurrenceMatrix(data)
        ndn = nbm.to_ndarray()
        sum = np.sum(ndn)
        sh = data.shape
        number_of_vertical_edges = 2 * 4
        number_of_horizontal_edges = 3 * 3
        self.assertEqual(sum, (number_of_horizontal_edges + number_of_vertical_edges) * 2)
        keys = nbm.keys()
        self.assertIn(0, keys)
        self.assertIn(1, keys)
        self.assertIn(2, keys)

        # print(nbm)
        # print data_out.shape
        # print data
        # print data_out
        # self.assertEquals(new_shape[0], data_out.shape[0])
        # self.assertEquals(new_shape[1], data_out.shape[1])
        # self.assertEquals(new_shape[2], data_out.shape[2])

    def test_neigh_matrix_obj_with_high_number(self):
        data = np.zeros((3, 4), dtype=int)
        data[:3, 1] = 1
        data[2:, 2] = 2
        data[0, 1:] = 6
        #
        nbm = imma.measure.CooccurrenceMatrix(data)
        ndn = nbm.to_ndarray()
        sum = np.sum(ndn)
        sh = data.shape
        number_of_vertical_edges = 2 * 4
        number_of_horizontal_edges = 3 * 3
        self.assertEqual(sum, (number_of_horizontal_edges + number_of_vertical_edges) * 2)
        keys = nbm.keys()
        self.assertIn(0, keys)
        self.assertIn(1, keys)
        self.assertIn(6, keys)

        inv_keys = nbm.inv_keys()
        key_in_table = inv_keys[6]
        six2zero_0 = ndn[inv_keys[6], inv_keys[0]]
        six2zero_1 = nbm.get(6, 0)
        self.assertEqual(six2zero_0, six2zero_1, "# 6 is neighboor of 0 ")

    def test_neigh_matrix_obj_not_return_counts(self):
        data = np.zeros((3, 4), dtype=int)
        data[:3, 1] = 1
        data[2:, 2] = 2
        data[0, 1:] = 3
        #
        nbm = imma.measure.CooccurrenceMatrix(data, return_counts=False)
        ndn = nbm.to_ndarray()
        sum = np.sum(ndn)
        self.assertLessEqual(np.max(ndn), 2)
        sh = data.shape
        # number_of_vertical_edges = 2 * 4
        # number_of_horizontal_edges = 3 * 3
        # self.assertEqual(sum, (number_of_horizontal_edges + number_of_vertical_edges) * 2)
        keys = nbm.keys()
        self.assertIn(0, keys)
        self.assertIn(1, keys)
        self.assertIn(2, keys)

    def test_element_neighboors(self):
        data = np.zeros((1, 3, 4), dtype=int)
        data[0, :3, 1] = 1
        data[0, 2:, 2] = 2
        data[0, 0, 1:] = 6
        # neighb, bbox = imma.measure.element_neighbors(data, 1)
        neighbs = imma.measure.objects_neighbors(data)
        print(neighbs)

        self.assertTrue(np.array_equal(neighbs[0], [0, 2, 6]), "Label 1 is negbor to [0, 2, 6]")
        self.assertTrue(np.array_equal(neighbs[1], [0, 1]), "Label 2 is negbor to [0, 1]")
        self.assertTrue(neighbs[3] is None, "Label 4 has no neighboor")
        self.assertTrue(np.array_equal(neighbs[5], [0, 1]), "Label 6 is negbor to [0, 1]")

    def test_element_neighboors_with_exclude(self):
        data = np.zeros((1, 3, 4), dtype=int)
        data[0, :3, 1] = 1
        data[0, 2:, 2] = 2
        data[0, 0, 1:] = 6
        # neighb, bbox = imma.measure.element_neighbors(data, 1)
        neighbs = imma.measure.objects_neighbors(data, exclude=[6])
        print(neighbs)

        self.assertTrue(np.array_equal(neighbs[0], [0, 2]), "Label 1 is negbor to [0, 2, 6]")
        self.assertTrue(np.array_equal(neighbs[1], [0, 1]), "Label 2 is negbor to [0, 1]")
        self.assertTrue(neighbs[3] is None, "Label 4 has no neighboor")
        self.assertTrue(np.array_equal(neighbs[5], [0, 1]), "Label 6 is negbor to [0, 1]")


if __name__ == "__main__":
    unittest.main()
