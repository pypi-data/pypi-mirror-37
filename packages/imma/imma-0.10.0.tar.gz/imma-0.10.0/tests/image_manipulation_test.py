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
import imma.image_manipulation as ima


class ImageManipulationTest(unittest.TestCase):
    interactivetTest = False

    # interactivetTest = True


    def test_seeds_inds(self):
        datap = io3d.datasets.generate_abdominal()
        seeds = datap["seeds"]
        data3d = datap["data3d"]
        sind = ima.as_seeds_inds(seeds, data3d.shape)
        self.assertGreater(seeds[sind][0], 0, "First found seed should be non zero")


if __name__ == "__main__":
    unittest.main()
