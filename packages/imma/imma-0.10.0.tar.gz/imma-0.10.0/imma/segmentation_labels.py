#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

import numpy as np
from . import dili


def get_nlabels(slab, labels, labels_meta=None, return_mode="num", return_first=False):
    """
    Get one or more labels, create a new one if necessary and return its numeric value.

    Look at the get_nlabel function for more details.

    :param slab:
    :param labels:
    :param labels_meta:
    :param return_mode: "num" or "str" or "both". Both means (numlabel, strlabel).
    :param return_first: Return just first found label
    :return:
    """

    if type(labels) not in (list, np.ndarray):
        labels = [labels]
        labels_meta = [labels_meta]
        return_first = True

    if labels_meta is None:
        labels_meta = [None] * len(labels)

    nlabels = []
    for label, label_meta in zip(labels, labels_meta):
        nlab = get_nlabel(slab, label, label_meta, return_mode=return_mode)
        nlabels.append(nlab)

    if return_first:
        nlabels = nlabels[0]
    return nlabels


def get_nlabel(slab, label, label_meta=None, return_mode="num"):
    """
    Add label if it is necessery and return its numeric value.

    If "new" keyword is used and no other information is provided, the max + 1 label is created.
    If "new" keyword is used and additional numeric info is provided, the number is used also as a key.
    :param return_mode: Set requested label return type. "int", "num", "numeric" or "str" or "both".
    "both" means (numlabel, strlabel).
    :param label: string, number or "new"
    :param label_meta: string, number or "new
    :return:
    """
    # todo add add_new and dont_add parameters to have fine control over adding new keys in slab
    numlabel = None
    strlabel = None
    if type(label) == str:
        if label_meta is None:
            if label not in slab.keys():
                free_numeric_label = np.max(list(slab.values())) + 1
                if label == "new":
                    label = str(free_numeric_label)
                slab[label] = free_numeric_label
                strlabel = label
                numlabel = slab[label]
            else:
                strlabel = label
                numlabel = slab[label]
        else:
            if label == "new":
                label = str(label_meta)
            update_slab(slab, label_meta, label)
            strlabel = label
            numlabel = label_meta
    else:
        # it is numeric
        if label_meta is None:
            if label not in list(slab.values()):
                update_slab(slab, label, str(label))
                strlabel = str(label)
            else:
                strlabel = dili.dict_find_key(slab, label)

            numlabel = label

        else:
            if label_meta == "new":
                label_meta = str(label)
            update_slab(slab, label, label_meta)
            strlabel = label_meta
            numlabel = label
            # return label

    if return_mode in ("num", "int", "numeric"):
        return numlabel
    elif return_mode == "str":
        return strlabel
    elif return_mode == "both":
        return numlabel, strlabel
    else:
        logger.error("Unknown return_mode: " + str(return_mode))


def update_slab(slab, numeric_label, string_label):
    """ Add label to segmentation label dictionary if it is not there yet.

    :param numeric_label:
    :param string_label:
    :return:
    """

    slab_tmp = {string_label: numeric_label}
    slab.update(slab_tmp)
    # slab = slab_tmp
    logger.debug('self.slab')
    logger.debug(str(slab))


def add_slab_label_carefully(slab, numeric_label, string_label):
    """ Add label to slab if it is not there yet.

    :param numeric_label:
    :param string_label:
    :return:
    """
    DeprecationWarning("Function will be removed in the future. Use get_nlabel instead.")
    get_nlabel(slab, numeric_label, string_label)


def add_missing_labels(segmentation, slab):
    labels = np.unique(segmentation)
    get_nlabels(slab, labels)

def minimize_slab(slab, segmentation, remove_doubled=True):
    """
    Check slab and kick out all not used or doubled values.
    :param slab:
    :param segmentation:
    :return:
    """
    un = np.unique(segmentation)
    unslab = np.unique(list(slab.values()))

    kick_labels = []
    keep_values = []
    for label in slab:
        val = slab[label]
        if val in un:
            if remove_doubled:
                if val in keep_values:
                    # it is doubled
                    kick_labels.append(val)
                else:
                    keep_values.append(label)
        else:
            kick_labels.append(label)

    for kicki in kick_labels:
        slab.pop(kicki)

    return slab

