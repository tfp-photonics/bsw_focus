#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import h5py
import argparse
import meep as mp
import numpy as np
from datetime import datetime
from util.bswfocus import BSWFocus
from util.geometry import meep_from_design_rotate
import matplotlib.pyplot as plt


def gauss_beam(k, sigma, pos):
    term1 = 2 * np.pi * 1j * pos.dot(k)
    term2 = pos.dot(pos) / (2 * sigma**2)
    return np.exp(term1 - term2)


def main(args):
    res = 20
    h5f = h5py.File(args.file, 'r')
    d = {k: h5f['sim'][k].value for k in h5f['sim'].keys()}
    m = np.array(h5f['design'])
    h5f.close()
    d.update({
        'sim_resolution': res,
    })
    d.update({
        'use_symmetry': True,
    })
    bsw = BSWFocus(**d)
    bsw.set_design(m[-1])

    k = mp.Vector3(0, 1, 0)
    bsw.sources = [mp.Source(mp.ContinuousSource(wavelength=bsw.wavelength,
                                                 width=bsw.source_width),
                             component=mp.Hz,
                             center=mp.Vector3(0, bsw.sy / 2),
                             size=mp.Vector3(bsw.cell[0], 0),
                             amp_func=lambda x: gauss_beam(k, args.sigma, x))]

    bsw.run()

    loc = '/home/yannick/data/rebuttal/gauss_beam/{}_sigma{:02d}_fields.h5'
    h5f = h5py.File(loc.format(
        os.path.splitext(os.path.basename(args.file))[0],
        int(args.sigma)), 'w')
    eps = bsw.sim.get_array(center=mp.Vector3(0, 0),
                            size=mp.Vector3(bsw.sx, bsw.sy),
                            component=mp.Dielectric)
    h5f['Dielectric'] = eps

    ex = bsw.sim.get_array(center=mp.Vector3(0, 0),
                           size=mp.Vector3(bsw.sx, bsw.sy),
                           component=mp.Ex)
    h5f['Ex'] = ex

    ey = bsw.sim.get_array(center=mp.Vector3(0, 0),
                           size=mp.Vector3(bsw.sx, bsw.sy),
                           component=mp.Ey)
    h5f['Ey'] = ey

    hz = bsw.sim.get_array(center=mp.Vector3(0, 0),
                           size=mp.Vector3(bsw.sx, bsw.sy),
                           component=mp.Hz)
    h5f['Hz'] = hz

    h5f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help="Input file(s)")
    parser.add_argument('-s', '--sigma', type=float, required=True,
                        help="Gaussian beam sigma")
    args = parser.parse_args()
    main(args)
