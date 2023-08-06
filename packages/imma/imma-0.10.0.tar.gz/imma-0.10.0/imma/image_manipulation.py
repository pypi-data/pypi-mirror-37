#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import os.path
import sys
import numpy as np
import scipy
import scipy.ndimage

from . import dili
from .image import as_seeds_inds, fit_to_shape, \
    combinecrinfo, crop, fix_crinfo, extend_crinfo, manualcrop, \
    resize_to_shape, random_rotate_paramteres, resize_to_mm, rotate, uncrop
from .labeled import select_labels, squeeze_labels, select_objects_by_seeds, crinfo_from_specific_data, \
    distance_segmentation, get_one_biggest_object, max_area_index
from .segmentation_labels import get_nlabel, add_missing_labels, add_slab_label_carefully, \
    get_nlabels, update_slab
from .sparse import isSparseMatrix, SparseMatrix

path_to_script = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(path_to_script, "../extern/sed3"))



# import sed3


