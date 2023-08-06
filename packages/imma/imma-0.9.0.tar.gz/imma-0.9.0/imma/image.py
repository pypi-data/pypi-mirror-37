#! /usr/bin/python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
import numpy as np
import scipy
import scipy.ndimage


def rotate(data3d, phi_deg, theta_deg=None, phi_axes=(1, 2), theta_axes=(0, 1), order=1, **kwargs):
    """
    Rotate 3D data by use angle and its axes or two angles.

    :param data3d: ndimage 3D
    :param phi_deg: deg
    :param phi_axes: deg
    :param theta_deg: deg
    :param theta_axes: deg
    :param order: optional, int. Default is 1. The order of the spline interpolation. See scipy for more details.
    :param kwargs: See scipy.ndimage.interpolation.rotate for more options
    :return:
    """

    data3d = scipy.ndimage.interpolation.rotate(data3d, phi_deg, phi_axes, order=order, **kwargs)
    if theta_deg is not None:
        data3d = scipy.ndimage.interpolation.rotate(data3d, theta_deg, theta_axes, order=order, **kwargs)
    return data3d
    # segmentation = scipy.ndimage.interpolation.rotate(segmentation, angle, axes)
    # seeds = scipy.ndimage.interpolation.rotate(seeds, angle, axes)


def random_rotate_paramteres():
    """
    Rotate data3d, segmentation and seeds with random rotation
    :return:
    """
    xi1 = np.random.rand()
    xi2 = np.random.rand()

    # theta = np.arccos(np.sqrt(1.0-xi1))
    theta = np.arccos(1.0 - (xi1 * 1))
    phi = xi2 * 2 * np.pi

    # xs = np.sin(theta) * np.cos(phi)
    # ys = np.sin(theta) * np.sin(phi)
    # zs = np.cos(theta)

    phi_deg = np.degrees(phi)
    theta_deg = np.degrees(theta)

    return phi_deg, theta_deg
    # TODO independent on voxlelsize (2016-techtest-rotate3d.ipynb)


def as_seeds_inds(seeds, datashape):
    shape = np.asarray(seeds).shape
    if datashape is not None and np.array_equal(shape, datashape):
        seeds_inds = np.nonzero(seeds)
    else:
        seeds_inds = seeds
    return seeds_inds


def resize_to_shape(data, shape, zoom=None, mode='reflect', order=0):
    """Resize input data to specific shape.

    :param data: input 3d array-like data
    :param shape: shape of output data
    :param zoom: zoom is used for back compatibility
    :mode: default is 'nearest'
    """
    # @TODO remove old code in except part

    if np.array_equal(data.shape, shape):
        return data

    try:
        # rint 'pred vyjimkou'
        # aise Exception ('test without skimage')
        # rint 'za vyjimkou'
        import skimage
        import skimage.transform
        # Now we need reshape  seeds and segmentation to original size

        segm_orig_scale = skimage.transform.resize(
            data, shape, order=order,
            preserve_range=True,
            mode=mode,
        )

        segmentation = segm_orig_scale
        logger.debug('resize to orig with skimage')
    except ImportError:
        DeprecationWarning("Resize by scipy will be removed in the future")
        mode = 'nearest'
        import scipy
        import scipy.ndimage
        dtype = data.dtype
        if zoom is None:
            zoom = np.asarray(data.shape).astype(np.double) / shape

        segm_orig_scale = scipy.ndimage.zoom(
            data,
            1.0 / zoom,
            mode=mode,
            order=order
        ).astype(dtype)
        logger.debug('resize to orig with scipy.ndimage')

        segmentation = fit_to_shape(segm_orig_scale, shape, dtype)
        del segm_orig_scale
    return segmentation


def fit_to_shape(segm_orig_scale, shape, dtype):
    # @TODO odstranit hack pro oříznutí na stejnou velikost
    # v podstatě je to vyřešeno, ale nechalo by se to dělat elegantněji v zoom
    # tam je bohužel patrně bug
    # rint 'd3d ', self.data3d.shape
    # rint 's orig scale shape ', segm_orig_scale.shape
    shp = [
        np.min([segm_orig_scale.shape[0], shape[0]]),
        np.min([segm_orig_scale.shape[1], shape[1]]),
        np.min([segm_orig_scale.shape[2], shape[2]]),
    ]
    # elf.data3d = self.data3d[0:shp[0], 0:shp[1], 0:shp[2]]
    # mport ipdb; ipdb.set_trace() # BREAKPOINT

    segmentation = np.zeros(shape, dtype=dtype)
    segmentation[:shp[0], :shp[1], :shp[2]] = segm_orig_scale[:shp[0], :shp[1], :shp[2]]

    return segmentation


def resize_to_mm(data3d, voxelsize_mm, new_voxelsize_mm, mode='reflect', order=1):
    """
    Function can resize data3d or segmentation to specifed voxelsize_mm
    :new_voxelsize_mm: requested voxelsize. List of 3 numbers, also
        can be a string 'orig', 'orig*2' and 'orig*4'.

    :voxelsize_mm: size of voxel
    :mode: default is 'edge'. Modes match the behaviour of numpy.pad
    """

    if new_voxelsize_mm is 'orig':
        new_voxelsize_mm = np.array(voxelsize_mm)

    elif new_voxelsize_mm is 'orig*2':
        new_voxelsize_mm = np.array(voxelsize_mm) * 2
    elif new_voxelsize_mm is 'orig*4':
        new_voxelsize_mm = np.array(voxelsize_mm) * 4
        # vx_size = np.array(metadata['voxelsize_mm']) * 4

    zoom = voxelsize_mm / (1.0 * np.array(new_voxelsize_mm))
    # data3d_res = scipy.ndimage.zoom(
    #     data3d,
    #     zoom,
    #     mode=mode,
    #     order=order
    # ).astype(data3d.dtype)

    # probably better implementation
    new_shape = data3d.shape * zoom
    import skimage.transform
    # Now we need reshape  seeds and segmentation to original size

    data3d_res2 = skimage.transform.resize(
        data3d, new_shape, order=order,
        mode=mode,
        preserve_range=True
    ).astype(data3d.dtype)

    return data3d_res2

def manualcrop(data):  # pragma: no cover

    try:
        from pysegbase import seed_editor_qt
    except:
        logger.warning("Deprecated of pyseg_base as submodule")
        import seed_editor_qt

    pyed = seed_editor_qt.QTSeedEditor(data, mode='crop')
    pyed.exec_()
    # pyed = sed3.sed3(data)
    # pyed.show()
    nzs = pyed.seeds.nonzero()
    crinfo = [
        [np.min(nzs[0]), np.max(nzs[0])],
        [np.min(nzs[1]), np.max(nzs[1])],
        [np.min(nzs[2]), np.max(nzs[2])],
    ]
    data = crop(data, crinfo)
    return data, crinfo


def crop(data, crinfo):
    """
    Crop the data.

    crop(data, crinfo)

    :param crinfo: min and max for each axis - [[minX, maxX], [minY, maxY], [minZ, maxZ]]

    """
    crinfo = fix_crinfo(crinfo)
    return data[
           __int_or_none(crinfo[0][0]):__int_or_none(crinfo[0][1]),
           __int_or_none(crinfo[1][0]):__int_or_none(crinfo[1][1]),
           __int_or_none(crinfo[2][0]):__int_or_none(crinfo[2][1])
           ]


def __int_or_none(number):
    if number is not None:
        number = int(number)
    return number


def combinecrinfo(crinfo1, crinfo2):
    """
    Combine two crinfos. First used is crinfo1, second used is crinfo2.
    """
    crinfo1 = fix_crinfo(crinfo1)
    crinfo2 = fix_crinfo(crinfo2)

    crinfo = [
        [crinfo1[0][0] + crinfo2[0][0], crinfo1[0][0] + crinfo2[0][1]],
        [crinfo1[1][0] + crinfo2[1][0], crinfo1[1][0] + crinfo2[1][1]],
        [crinfo1[2][0] + crinfo2[2][0], crinfo1[2][0] + crinfo2[2][1]]
    ]

    return crinfo


def extend_crinfo(crinfo, shape, margin):
    crinfo = fix_crinfo(crinfo, with_slices=True)
    d0 = max(0, crinfo[0].start - margin)
    u0 = min(shape[0], crinfo[0].stop + margin)
    slice_z = slice(d0, u0)
    d1 = max(0, crinfo[1].start - margin)
    u1 = min(shape[1], crinfo[1].stop + margin)
    slice_y = slice(d1, u1)
    d2 = max(0, crinfo[2].start - margin)
    u2 = min(shape[2], crinfo[2].stop + margin)
    slice_x = slice(d2, u2)
    crinfoo = (slice_z, slice_y, slice_x)
    return crinfoo



def uncrop(data, crinfo, orig_shape, resize=False, outside_mode="constant", cval=0):
    """
    Put some boundary to input image.


    :param data: input data
    :param crinfo: array with minimum and maximum index along each axis
        [[minX, maxX],[minY, maxY],[minZ, maxZ]]. If crinfo is None, the whole input image is placed into [0, 0, 0].
        If crinfo is just series of three numbers, it is used as an initial point for input image placement.
    :param orig_shape: shape of uncropped image
    :param resize: True or False (default). Usefull if the data.shape does not fit to crinfo shape.
    :param outside_mode: 'constant', 'nearest'
    :return:
    """

    if crinfo is None:
        crinfo = list(zip([0] * data.ndim, orig_shape))
    elif np.asarray(crinfo).size == data.ndim:
        crinfo = list(zip(crinfo, np.asarray(crinfo) + data.shape))

    crinfo = fix_crinfo(crinfo)
    data_out = np.ones(orig_shape, dtype=data.dtype) * cval

    # print 'uncrop ', crinfo
    # print orig_shape
    # print data.shape
    if resize:
        data = resize_to_shape(data, crinfo[:, 1] - crinfo[:, 0])

    startx = np.round(crinfo[0][0]).astype(int)
    starty = np.round(crinfo[1][0]).astype(int)
    startz = np.round(crinfo[2][0]).astype(int)

    data_out[
    # np.round(crinfo[0][0]).astype(int):np.round(crinfo[0][1]).astype(int)+1,
    # np.round(crinfo[1][0]).astype(int):np.round(crinfo[1][1]).astype(int)+1,
    # np.round(crinfo[2][0]).astype(int):np.round(crinfo[2][1]).astype(int)+1
    startx:startx + data.shape[0],
    starty:starty + data.shape[1],
    startz:startz + data.shape[2]
    ] = data

    if outside_mode == "nearest":
        # for ax in range(data.ndims):
        # ax = 0

        # copy border slice to pixels out of boundary - the higher part
        for ax in range(data.ndim):
            # the part under the crop
            start = np.round(crinfo[ax][0]).astype(int)
            slices = [slice(None), slice(None), slice(None)]
            slices[ax] = start
            repeated_slice = np.expand_dims(data_out[slices], ax)
            append_sz = start
            if append_sz > 0:
                tile0 = np.repeat(repeated_slice, append_sz, axis=ax)
                slices = [slice(None), slice(None), slice(None)]
                slices[ax] = slice(None, start)
                # data_out[start + data.shape[ax] : , :, :] = tile0
                data_out[slices] = tile0
                # plt.imshow(np.squeeze(repeated_slice))
                # plt.show()

            # the part over the crop
            start = np.round(crinfo[ax][0]).astype(int)
            slices = [slice(None), slice(None), slice(None)]
            slices[ax] = start + data.shape[ax] - 1
            repeated_slice = np.expand_dims(data_out[slices], ax)
            append_sz = data_out.shape[ax] - (start + data.shape[ax])
            if append_sz > 0:
                tile0 = np.repeat(repeated_slice, append_sz, axis=ax)
                slices = [slice(None), slice(None), slice(None)]
                slices[ax] = slice(start + data.shape[ax], None)
                # data_out[start + data.shape[ax] : , :, :] = tile0
                data_out[slices] = tile0
                # plt.imshow(np.squeeze(repeated_slice))
                # plt.show()

    return data_out


def fix_crinfo(crinfo, to='axis', with_slices=False):
    """
    Function recognize order of crinfo and convert it to proper format.
    """

    if type(crinfo[0]) is slice:
        if with_slices:
            return crinfo
        else:
            crinfo = [
                [crinfo[0].start, crinfo[0].stop],
                [crinfo[1].start, crinfo[1].stop],
                [crinfo[2].start, crinfo[2].stop],
            ]
    else:
        crinfo = np.asarray(crinfo)
        if crinfo.shape[0] == 2:
            crinfo = crinfo.T

        if with_slices:
            crinfo = (
                slice(crinfo[0][0], crinfo[0][1]),
                slice(crinfo[1][0], crinfo[1][1]),
                slice(crinfo[2][0], crinfo[2][1])
            )
        else:
            pass

    return crinfo
