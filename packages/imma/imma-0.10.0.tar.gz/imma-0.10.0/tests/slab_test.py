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
import imma.segmentation_labels as imsl


class ImageManipulationTest(unittest.TestCase):
    interactivetTest = False

    def test_get_nlabels(self):
        datap = io3d.datasets.generate_abdominal()
        data3d = datap["data3d"]
        segmentation = datap["segmentation"]
        newlab = imsl.get_nlabels(datap["slab"], "new", return_mode="str")
        self.assertEqual(type(newlab), str)

    def test_get_nlabel_new(self):
        datap = io3d.datasets.generate_abdominal()
        data3d = datap["data3d"]
        segmentation = datap["segmentation"]
        newlab = imsl.get_nlabel(datap["slab"], "new", return_mode="str")
        self.assertEqual(type(newlab), str)

        newlab = imsl.get_nlabel(datap["slab"], "new", 37, return_mode="str")
        self.assertEqual(type(newlab), str, "new label with defined number value")
        self.assertEqual(newlab, "37")

        newlab = imsl.get_nlabel(datap["slab"], 38, "new", return_mode="str")
        self.assertEqual(type(newlab), str, "new label with defined number value")
        self.assertEqual(newlab, "38")

        newlab = imsl.get_nlabel(datap["slab"], "new", return_mode="num")
        self.assertTrue(np.issubdtype(type(newlab), np.integer))

    def test_add_missing_label(self):
        datap = io3d.datasets.generate_abdominal()
        data3d = datap["data3d"]
        segmentation = datap["segmentation"]
        slab = datap["slab"]
        slab = {"none": 0, "liver": 1}
        imsl.add_missing_labels(segmentation, slab)
        self.assertGreater(len(slab), 2)

    def test_simple_get_nlabel(self):
        slab = {"liver": 1, "porta": 2}
        val = imsl.get_nlabel(slab, 2)
        self.assertEqual(val, 2)
        self.assertEqual(len(slab), 2)

    def test_simple_string_get_nlabel(self):
        slab = {"liver": 1, "porta": 2}
        val = imsl.get_nlabel(slab, "porta")
        self.assertEqual(val, 2)
        self.assertEqual(len(slab), 2)

    def test_simple_new_numeric_get_nlabel(self):
        slab = {"liver": 1, "porta": 2}
        val = imsl.get_nlabel(slab, 7)
        self.assertNotEqual(val, 1)
        self.assertNotEqual(val, 2)
        self.assertEqual(val, 7)

    def test_simple_new_string_get_nlabel(self):
        slab = {"liver": 1, "porta": 2}
        val = imsl.get_nlabel(slab, "cava")
        self.assertNotEqual(val, 1)
        self.assertNotEqual(val, 2)

    def test_simple_add_carefully(self):
        slab = {"liver": 1, "porta": 2}
        imsl.add_slab_label_carefully(slab, 5, "cava")
        self.assertEqual(slab["cava"], 5)

    def test_simple_string_get_nlabel_return_string(self):
        slab = {"liver": 1, "porta": 2}
        val = imsl.get_nlabel(slab, "porta", return_mode="str")
        self.assertEqual(val, "porta")

    def test_simple_numeric_get_nlabel_return_string(self):
        slab = {"liver": 1, "porta": 2}
        val = imsl.get_nlabel(slab, 2, return_mode="str")
        self.assertEqual(val, "porta")

    def test_get_nlabels_single_label(self):
        slab = {"liver": 1, "kindey": 15, "none": 0}
        labels = 1
        val = imsl.get_nlabels(slab, labels)
        self.assertEqual(val, 1)

    def test_get_nlabels_multiple(self):
        slab = {"liver": 1, "porta": 2}
        val = imsl.get_nlabels(slab, [2, "porta", "new", 7], return_mode="str")
        self.assertEqual(val[0], "porta")
        self.assertEqual(val[1], "porta")
        self.assertEqual(val[2], "3")
        self.assertEqual(val[3], "7")

    def test_get_nlabels_single(self):
        slab = {"liver": 1, "porta": 2}

        val = imsl.get_nlabels(slab, "porta", return_mode="int")
        self.assertEqual(val, 2)

    def test_get_nlabels_single_both(self):
        slab = {"liver": 1, "porta": 2}

        val = imsl.get_nlabels(slab, "porta", return_mode="both")
        self.assertEqual(val[0], 2)
        self.assertEqual(val[1], "porta")

    def test_minimize_slab(self):
        segmentation = np.zeros([5, 5])
        segmentation[:3, :2] = 1
        segmentation[3:, :3] = 5

        slab = {
            "label1": 1,
            "label2": 2,
            "label5": 5,
            "label22": 2
        }

        slab = imsl.minimize_slab(slab, segmentation)

        self.assertEqual(len(slab), 2)
        self.assertTrue(np.array_equal(list(slab.values()), [1, 5]))


if __name__ == "__main__":
    unittest.main()
