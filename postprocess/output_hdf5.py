#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import h5py
import argparse
import meep as mp
import numpy as np
from datetime import datetime
from util.bswfocus import BSWFocus


def main(args):
    fields, epsilons, fnames = [], [], []
    for fname in args.file:
        h5f = h5py.File(fname, 'r')
        d = {k: h5f['sim'][k].value for k in h5f['sim'].keys()}
        m = np.array(h5f['design'])
        h5f.close()
        res = 20
        d.update({
            'sim_resolution': res,
        })
        bsw = BSWFocus(**d)
        bsw.set_design(m[-1])
        bsw.run()

        h5f = h5py.File('/scratch/local/data/fields/{}_fields.h5'.format(os.path.splitext(os.path.basename(fname))[0], 'w'))

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
    parser.add_argument('-f', '--file', type=str, nargs='+', required=True,
                        help="Input file(s)")
    args = parser.parse_args()
    main(args)
