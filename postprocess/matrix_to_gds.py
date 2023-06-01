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
from gdshelpers.parts.text import Text
from gdshelpers.helpers import id_to_alphanumeric
from gdshelpers.geometry import convert_to_gdscad, geometric_union

from util.bswfocus import BSWFocus


def parse_cmdline():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, nargs='+', required=True,
                        help="Input file(s)")
    parser.add_argument('--save', action='store_true',
                        help="Save output (gds & id file)")
    parser.add_argument('--show', action='store_true',
                        help="Show output as plot")
    parser.add_argument('--dist', type=float, default=300,
                        help="Distance between designs (micrometers)")
    parser.add_argument('--ncols', type=int, default=4,
                        help="Number of columns per row")
    return parser.parse_args()


def get_cell(fname, col, row, layer, dist):
    h5f = h5py.File(fname, 'r')
    d = {k: h5f['sim'][k].value for k in h5f['sim'].keys()}
    design = np.fliplr(h5f['design'][-1])
    box_intensity = float(np.array(h5f['focus'][-1]))
    fwhm = float(np.array(h5f['fwhm']))
    fwhm_intensity = float(np.array(h5f['fwhm_intensity']))
    h5f.close()

    dn = round(d['n_hi'] - d['n_lo'], 3)

    dx, dy = col * dist, row * dist

    spacing = float(d['spacing'])
    sx = np.abs(float(d['design_xr'][1]) - float(d['design_xr'][0]))
    sy = np.abs(float(d['design_yr'][1]) - float(d['design_yr'][0]))
    nx, ny = design.shape[0], design.shape[1]
    cx, cy = np.mean([0, sx]) + dx, np.mean([0, sy]) + dy
    width = np.round(sx / nx, 2) - spacing
    height = np.round(sy / ny, 2) - spacing
    px, py = width + spacing, height + spacing
    x_range = np.linspace(cx - px * (nx - 1) / 2, cx + px * (nx - 1) / 2, nx)
    y_range = np.linspace(cy - py * (ny - 1) / 2, cy + py * (ny - 1) / 2, ny)
    shapes = []
    for i, j in np.transpose(np.where(design == 1)):
        x0, x1 = x_range[i] - width / 2., x_range[i] + width / 2.
        y0, y1 = y_range[j] - height / 2., y_range[j] + height / 2.
        bx = box(x0, y0, x1, y1)
        shapes.append(bx)
    anum = id_to_alphanumeric(col, row)
    cell = Cell(anum)
    text = Text([-dist / 3. + dx, sy + dy], 4, anum)
    cell.add(convert_to_gdscad(text, layer=0))
    cell.add(convert_to_gdscad(shapes, layer=layer))
    return cell, anum, int(cx), int(cy), box_intensity, fwhm, fwhm_intensity, dn


def main(args):
    layout = Layout()
    id_table = []
    shapes = []
    dist = args.dist
    ncols = args.ncols
    nrows = len(args.file) / ncols

    for sector in range(4):
        layer = sector + 1
        for jj in range(2):
            for ii, name in enumerate(args.file):
                col = (ii % ncols + (sector % 2) * (ncols + 1)) + (jj + sector % 2) * ncols
                row = (ii // ncols + (sector // 2) * (nrows + 1))
                cell, anum, cx, cy, intensity, fwhm, fwhm_int, dn = get_cell(name, col, row, layer, dist)
                id_table.append([anum, cx, cy, layer, dn, intensity, fwhm, fwhm_int, splitext(basename(name))[0]])
                layout.add(cell)

    if args.save:
        tstamp = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
        layout.save('{}.gds'.format(tstamp))
        with open('{}_ids.txt'.format(tstamp), 'w') as f:
            for row in id_table:
                print(' '.join(str(cell) for cell in row), file=f)
            f.close()

    if args.show:
        layout.show()


if __name__ == '__main__':
    args = parse_cmdline()
    main(args)
