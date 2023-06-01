#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import argparse
from os.path import basename, splitext
from datetime import datetime

import h5py
import numpy as np

from shapely.geometry import box
from gdsCAD.core import Cell, Layout
from gdshelpers.geometry import convert_to_gdscad


def parse_cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files', type=str, nargs='+', required=True,
                        help="Input file(s)")
    parser.add_argument('-b', '--border', type=float, default=0,
                        help="Border around structure in um")
    parser.add_argument('--show', action='store_true',
                        help="Show output as plot")
    return parser.parse_args()


def main():
    args = parse_cmdline()
    for fname in args.files:
        h5f = h5py.File(fname, 'r')
        d = {k: h5f['sim'][k].value for k in h5f['sim'].keys()}
        design = np.fliplr(h5f['design'][-1])
        h5f.close()

        spacing = float(d['spacing'])
        sx = np.abs(float(d['design_xr'][1]) - float(d['design_xr'][0]))
        sy = np.abs(float(d['design_yr'][1]) - float(d['design_yr'][0]))
        nx, ny = design.shape[0], design.shape[1]
        cx, cy = np.mean([0, sx]), np.mean([0, sy])
        width = np.round(sx / nx, 2) - spacing
        height = np.round(sy / ny, 2) - spacing
        px, py = width + spacing, height + spacing
        x_range = np.linspace(cx - px * (nx - 1) / 2,
                              cx + px * (nx - 1) / 2, nx)
        y_range = np.linspace(cy - py * (ny - 1) / 2,
                              cy + py * (ny - 1) / 2, ny)
        shapes = []
        for i, j in np.transpose(np.where(design == 1)):
            x0, x1 = x_range[i] - width / 2., x_range[i] + width / 2.
            y0, y1 = y_range[j] - height / 2., y_range[j] + height / 2.
            bx = box(x0, y0, x1, y1)
            shapes.append(bx)
        cell = Cell('')
        cell.add(convert_to_gdscad(shapes, layer=0))

        layout = Layout()
        layout.add(cell)
        layout.save('{}.gds'.format(splitext(basename(fname))[0]))

        if args.show:
            layout.show()


if __name__ == '__main__':
    main()
