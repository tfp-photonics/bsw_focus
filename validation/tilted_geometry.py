#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import h5py
import argparse
import meep as mp
import numpy as np
from datetime import datetime
from util.bswfocus import BSWFocus
from util.geometry import meep_from_design_rotate
import matplotlib.pyplot as plt


def main(args):
    x_pad = 4
    res = 20
    h5f = h5py.File(args.file, 'r')
    d = {k: h5f['sim'][k].value for k in h5f['sim'].keys()}
    m = np.array(h5f['design'])
    h5f.close()
    d.update({
        'sim_resolution': res,
    })
    d.update({
        'use_symmetry': False,
    })
    d.update({
        'cell_pad_x': x_pad,
    })
    bsw = BSWFocus(**d)
    bsw.set_design(meep_from_design_rotate(m[-1],
                                           bsw.design_xr,
                                           bsw.design_yr,
                                           bsw.eps_hi, args.tilt))

    bsw.run()

    # loc = '/scratch/local/paper_data/rebuttal/{}_tilt{}_fields.h5'
    loc = '/home/yannick/data/rebuttal/source_tilt/{}_tilt{:02d}_fields.h5'
    h5f = h5py.File(loc.format(
        os.path.splitext(os.path.basename(args.file))[0],
        int(args.tilt)), 'w')
    eps = bsw.sim.get_array(center=mp.Vector3(0, 0),
                            size=mp.Vector3(bsw.sx + 2 * x_pad, bsw.sy),
                            component=mp.Dielectric)
    h5f['Dielectric'] = eps

    ex = bsw.sim.get_array(center=mp.Vector3(0, 0),
                           size=mp.Vector3(bsw.sx + 2 * x_pad, bsw.sy),
                           component=mp.Ex)
    h5f['Ex'] = ex

    ey = bsw.sim.get_array(center=mp.Vector3(0, 0),
                           size=mp.Vector3(bsw.sx + 2 * x_pad, bsw.sy),
                           component=mp.Ey)
    h5f['Ey'] = ey

    hz = bsw.sim.get_array(center=mp.Vector3(0, 0),
                           size=mp.Vector3(bsw.sx + 2 * x_pad, bsw.sy),
                           component=mp.Hz)
    h5f['Hz'] = hz

    h5f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, required=True,
                        help="Input file(s)")
    parser.add_argument('-t', '--tilt', type=float, required=True,
                        help="Tilt of the structure")
    args = parser.parse_args()
    main(args)
