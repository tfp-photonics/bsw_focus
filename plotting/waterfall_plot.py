#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, re
from argparse import ArgumentParser
from datetime import datetime
import h5py
import numpy as np
from matplotlib import rcParams
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt


def polygon_under_graph(xlist, ylist):
    return [(xlist[0], 0.)] + list(zip(xlist, ylist)) + [(xlist[-1], 0.)]


def get_xdist(field, norm=True):
    col = field[(field.shape[0] // 2 - 10):(field.shape[0] // 2 + 10), :]
    y_mean = np.mean(col, axis=0)
    y_max_idx = int(np.mean(np.where(y_mean == np.max(y_mean))[0]))
    x_dist = field[:, y_max_idx]
    x_dist = np.mean(field[:, y_max_idx - 10:y_max_idx + 10], axis=1)
    if norm:
        x_dist /= np.max(x_dist)
    return x_dist


def load_files(files):
    eps_dims = []
    x_dists = []
    p = re.compile('[0-9]+x[0-9]+')
    for fname in args.files:
        h5f = h5py.File(fname, 'r')
        ex = np.asarray(h5f['Ex'])
        ey = np.asarray(h5f['Ey'])
        h5f.close()
        field = np.square(np.abs(ex)) + np.square(np.abs(ey))
        x_dists.append(get_xdist(field, norm=False))
        eps_dims.append(p.search(fname).group(0))
    return np.array(x_dists), np.array(eps_dims)


def main(args):
    x_dists, eps_dims = load_files(args.files)

    pgf_with_custom_preamble = {
        'font.family': 'sans-serif',
        # 'font.sans-serif': 'Helvetica Neue',
        'text.usetex': True,
        'pgf.rcfonts': True,
        'pgf.preamble': [
            r'\usepackage[utf8]{inputenc}',
            r'\usepackage{amsmath}',
            r'\usepackage{siunitx}',
            r'\usepackage{physics}',
            r'\usepackage{unicode-math}',
        ]
    }
    rcParams.update(pgf_with_custom_preamble)

    fig = plt.figure()
    ax = fig.gca(projection='3d')

    verts = []
    for ys in x_dists:
        verts.append(polygon_under_graph(range(len(ys)), ys))
    colors = plt.get_cmap('viridis')(np.linspace(0, 1, len(verts)))[::-1]
    poly = PolyCollection(verts,
                          facecolors=colors,
                          edgecolors='k',
                          linewidths=0.4,
                          alpha=0.8)
    ax.add_collection3d(poly, zs=range(len(verts)), zdir='y')
    ax.set_xlim3d(0, x_dists[0].shape[0])
    ax.set_ylim3d(0, len(verts))
    ax.set_zlim3d(0, np.max(x_dists))
    ax.set_xticks(np.linspace(0, x_dists[0].shape[0], 5))
    ax.set_xticklabels(np.linspace(-(x_dists[0].shape[0] - 1) / 40,
                                   (x_dists[0].shape[0] - 1) / 40,
                                   5, dtype=int))
    ax.set_yticks([0, 5, 10, 12])
    ax.set_yticklabels(eps_dims[[0, 5, 10, 12]])
    ax.set_xlabel(r'x-axis ($\mu m$)', fontsize=10)
    ax.set_ylabel(r'Grid resolution', fontsize=10)
    ax.set_zlabel(r'Intensity (a.u.)', fontsize=10)

    ax.view_init(elev=25, azim=-75)

    if args.save is not None:
        tstamp = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
        name = '_waterfall'
        path = os.path.join(args.save, tstamp + name + os.extsep + args.ext)
        plt.savefig(path, dpi=300, bbox_inches='tight')
    else:
        plt.show()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-f', '--files', type=str, nargs='+',
                        required=True, help="Dataset files")
    parser.add_argument('-s', '--save', type=str, default=None, nargs='?',
                        const='', required=False, help="Save plots")
    parser.add_argument('-e', '--ext', type=str, default='pdf',
                        required=False, help="Output filetype")
    args = parser.parse_args()
    main(args)
