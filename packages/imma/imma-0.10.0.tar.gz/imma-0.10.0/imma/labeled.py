#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import numpy as np
import scipy

from . import segmentation_labels
ima = segmentation_labels

def select_labels(segmentation, labels, slab=None):
    """
    return ndimage with zeros and ones based on input labels

    :param segmentation: 3D ndimage
    :param labels: labels to select
    :param slab: dictionary{string_label: numeric_label}. Allow to use
    string labels if it is defined
    :return:
    """

    if slab is not None:
        labels = segmentation_labels.get_nlabels(slab, labels)

    if type(labels) not in (list, np.ndarray, set):
        labels = [labels]

    ds = np.zeros(segmentation.shape, np.bool)
    for lab in labels:
        dadd = (segmentation == lab)

        ds = ds | dadd
    if len(labels) == 0:
        logger.warning("Labels not found in slab.")

    return ds


def get_one_biggest_object(data):
    """ Return biggest object """
    lab, num = scipy.ndimage.label(data)
    # print ("bum = "+str(num))

    maxlab = max_area_index(lab, num)

    data = (lab == maxlab)
    return data


def max_area_index(labels, num=None):
    """
    Return index of maxmum labeled area
    """
    mx = 0
    mxi = -1
    un = np.unique(labels)
    # kick out zero
    un = un[un != 0]
    for l in un:
        mxtmp = np.sum(labels == l)
        if mxtmp > mx:
            mx = mxtmp
            mxi = l

    return mxi


def max_area_index2(labels, num):
    """
    Return index of maxmum labeled area. Old implementation. Slower.
    """
    DeprecationWarning("Function will be removed in future")
    mx = 0
    mxi = -1
    for l in range(1, num + 1):
        mxtmp = np.sum(labels == l)
        if mxtmp > mx:
            mx = mxtmp
            mxi = l

    return mxi




def select_objects_by_seeds(binar_data, seeds, ignore_background_seeds=True, background_label=0):
    """
    Get N biggest objects from the selection or the object with seed.

    :param binar_data:  binar ndarray
    :param seeds: ndarray. Objects on non zero positions are returned
    :return:
    """

    labeled_data, length = scipy.ndimage.label(binar_data)
    selected_labels = list(np.unique(labeled_data[seeds > 0]))
    # selected_labels.pop(0)
    # pop the background label
    output = np.zeros_like(binar_data)
    for label in selected_labels:
        selection = labeled_data == label
        # copy from input image to output. If there will be seeds in background, the 0 is copied
        if ignore_background_seeds and (binar_data[selection][0] == background_label):
            pass
        else:
            # output[selection] = binar_data[selection]
            output[selection] = 1
    # import sed3
    # ed =sed3.sed3(labeled_data, contour=output, seeds=seeds)
    # ed.show()
    return output



def squeeze_labels(segmentation, try_inplace=True):
    """
    Squeeze all labels to int numbers starting from 1

    :param segmentation: labeled image
    :param try_inplace: try to compute inplace
    :return:
    """
    un = np.unique(segmentation)

    if try_inplace:
        inplace_possible = True
        for new_level, level in enumerate(un):
            # if i == level:
            #     continue
            if (new_level > level) and (new_level in un):
                # we will rewrite old
                inplace_possible = False
                break
    else:
        inplace_possible = False

    if inplace_possible:
        output = segmentation
    else:
        import copy
        output = copy.copy(segmentation)

    for new_level, level in enumerate(un):
        output[segmentation == level] = new_level

    return output


def distance_segmentation(seeds, method="edt"):
    """
    Separates space based on distance to seeds.
    :param seeds: ndarray with zeros for background and labeled seeds.
    :param method: scipy.ndimage.distance_transform function.
    The `distance_transform_edt` is used if is set to "edt"
    :return:
    """
    if method is "edt":
        dst_transform = scipy.ndimage.distance_transform_edt
    else:
        dst_transform = method

    inds = dst_transform(seeds == 0, return_indices=True, return_distances=False)

    lin_inds = []
    for one_ax in inds:
        lin_inds.append(one_ax.ravel())

    segm = seeds[lin_inds].reshape(seeds.shape)
    return segm

    pass

def crinfo_from_specific_data(data, margin=0, with_slices=False):
    """
    Create crinfo of minimum orthogonal nonzero block in input data.

    :param data: input data
    :param margin: add margin to minimum block
    :return:
    """
    # hledáme automatický ořez, nonzero dá indexy
    logger.debug('crinfo')
    logger.debug(str(margin))
    nzi = np.nonzero(data)
    logger.debug(str(nzi))

    if np.isscalar(margin):
        margin = [margin] * 3

    x1 = np.min(nzi[0]) - margin[0]
    x2 = np.max(nzi[0]) + margin[0] + 1
    y1 = np.min(nzi[1]) - margin[0]
    y2 = np.max(nzi[1]) + margin[0] + 1
    z1 = np.min(nzi[2]) - margin[0]
    z2 = np.max(nzi[2]) + margin[0] + 1

    # ošetření mezí polí
    if x1 < 0:
        x1 = 0
    if y1 < 0:
        y1 = 0
    if z1 < 0:
        z1 = 0

    if x2 > data.shape[0]:
        x2 = data.shape[0] - 1
    if y2 > data.shape[1]:
        y2 = data.shape[1] - 1
    if z2 > data.shape[2]:
        z2 = data.shape[2] - 1

    # ořez
    if with_slices:
        crinfo = (slice(x1, x2), slice(y1, y2), slice(z1, z2))
    else:
        crinfo = [[x1, x2], [y1, y2], [z1, z2]]
    return crinfo


def unique_labels_by_seeds(labeled, seeds, ignored_seeds=0):
    """
    Get labels on positions of seeds.
    :param labeled: labeled ndimage
    :param seeds: ndimage with seeds
    :param ignored_seeds: int or list with labels to ignore, default ignored seed is 0
    :return: Dictionary. Keys are seeds, values are unique labels corresponding to this seeds.
    """

    if type(ignored_seeds) is not list:
        ignored_seeds = [ignored_seeds]
    # un = np.unique(seeds)
    # output = [None] * len(un)
    output = {}
    for seed in np.unique(seeds):
        if seed not in ignored_seeds:
            output[seed] = np.unique(labeled[seeds == seed])

    return output

