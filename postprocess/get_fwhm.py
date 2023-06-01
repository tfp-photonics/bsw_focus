#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from os.path import basename
import numpy as np
import h5py
from scipy.io import loadmat
from scipy.interpolate import UnivariateSpline
from scipy.ndimage import rotate


def get_fwhm(axis_slice, resolution=20):
    cx = np.mean(np.where(axis_slice == axis_slice.max()))
    fy = axis_slice[int(cx - 8 * resolution):
                    int(cx + 8 * resolution)]
    fx = np.linspace(0, fy.shape[0] / resolution, fy.shape[0])
    spline = UnivariateSpline(fx, fy - np.max(fy) / 2, s=0)
    try:
        r1, r2 = spline.roots()
        fwhm = np.abs(r2 - r1)
    except ValueError:
        fwhm = np.nan
    return fwhm, np.max(axis_slice)


def get_slice(field, axis=0, norm=True):
    max_y, max_x = np.where(field == field.max())
    axis_slice = None
    if axis == 0:
        axis_slice = field[int(np.mean(max_y)), :]
    else:
        axis_slice = field[:, int(np.mean(max_x))]
    if norm:
        axis_slice /= np.max(axis_slice)
    return axis_slice


def load_sim(fname, rotate_deg=None):
    h5f = h5py.File(fname, 'r')
    ex = np.asarray(h5f['Ex']).T
    h5f.close()
    ex = np.square(np.abs(ex))
    if rotate_deg is not None:
        pivot = np.array((ex.shape[0] / 2, ex.shape[1] / 2 + 315), dtype=int)
        padX = [ex.shape[1] - pivot[0], pivot[0]]
        padY = [ex.shape[0] - pivot[1], pivot[1]]
        ex = np.pad(ex, [padY, padX], 'constant')
        ex = rotate(ex, rotate_deg, reshape=False)
        ex = ex[padY[0]+400:-padY[1]-120, padX[0]+70:-padX[1]-70]
    return ex


def load_snom(fname):
    h5f = h5py.File(fname, 'r')
    intensity = np.asarray(h5f['intensity_close']).T
    h5f.close()
    return np.square(np.abs(intensity))


def load_files(files):
    x_slices, y_slices = [], []
    for fname in args.files:
        if 'snom' in fname:
            field = load_snom(fname)
        else:
            field = load_sim(fname)
        x_slices.append(get_slice(field, axis=0, norm=False))
        y_slices.append(get_slice(field, axis=1, norm=False))
    return np.array(x_slices), np.array(y_slices)


def main(args):
    x_slices, y_slices = load_files(args.files)
    results = []

    for name, x_slice, y_slice in zip(args.files, x_slices, y_slices):
        lateral_fwhm, intensity = get_fwhm(x_slice, args.resolution)
        axial_fwhm, _ = get_fwhm(y_slice, args.resolution)
        results.append([basename(name), lateral_fwhm, axial_fwhm, intensity])

    print('simulation lateral_fwhm axial_fwhm intensity')
    for row in results:
        print(*row, sep=' ')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--files', type=str, nargs='+',
                        required=True, help="Dataset files")
    parser.add_argument('-r', '--resolution', type=int, default=20,
                        help="Simulation resolution")
    args = parser.parse_args()
    main(args)
