#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import h5py
import argparse
import numpy as np
from ..util.bswfocus import BSWFocus
from ..util.plotter import *
from ..util.geometry import make_isosceles


def main(args):
    h5f = h5py.File(args.file, 'r')
    d = {k: h5f['sim'][k].value for k in h5f['sim'].keys()}
    m = np.array(h5f['design'])
    e = np.array(h5f['focus'])
    t = np.array(h5f['it_time'])
    h5f.close()

    d.update({
        'sim_resolution': args.res,
    })

    bsw = BSWFocus(**d)
    bsw.set_design(m[-1])

    if args.tri != 0:
        basename = None
        bsw.set_design(make_isosceles((-5, 5), (24, 24 - args.tri), 1.3))
        yr = (-25, 24 - args.tri - 0.5)
    else:
        fn = os.path.basename(args.file)
        basename = os.path.splitext(fn)[0]
        yr = (-25, np.max(bsw.focus_yr))

    bsw.run()

    plot_with_eps(bsw, fname=basename, savefig=args.save)
    # plot_intensities(bsw, fname=basename, savefig=args.save)
    plot_focus(bsw, sx=3, yr=yr, fname=basename, savefig=args.save)
    # plot_stats(e, t, fname=basename, savefig=args.save)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, default="",
                        help="Dataset file")
    parser.add_argument('-r', '--res', type=int, default=10,
                        help="Resolution for plotting simulation")
    parser.add_argument('-t', '--tri', type=int, default=0,
                        help="Use triangle of given height instead of sim design.")
    parser.add_argument('-s', '--save', type=str, default='',
                        help="Save plots")
    args = parser.parse_args()
    main(args)
