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

    raw_data = np.loadtxt(
        '/scratch/local/rebuttal/simulation_data_neff.txt',
        skiprows=1, unpack=True)

    data = []
    for wvl in range(1250, 1660, 10):
        data.append(raw_data[:, np.where(raw_data == wvl)[1]])

    for (wvl, n_lo, n_hi) in data:
        d.update({
            'n_lo': n_lo[0],
        })
        d.update({
            'n_hi': n_hi[0],
        })
        d.update({
            'wavelength': wvl[0] / 1000,
        })
        bsw = BSWFocus(**d)
        bsw.set_design(m[-1])

        bsw.run()

        loc = '/scratch/local/rebuttal/wvlen_sweep/{}_wvlen{}_fields.h5'
        h5f = h5py.File(loc.format(
            os.path.splitext(os.path.basename(args.file))[0],
            int(wvl[0])), 'w')
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
    args = parser.parse_args()
    main(args)
