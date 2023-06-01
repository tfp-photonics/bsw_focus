#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import h5py
import time
import argparse
import meep as mp
import numpy as np
from datetime import datetime as dt
from multiprocessing import Pool
from util.bswfocus import BSWFocus

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dim', type=int, required=True,
                    help="Dimension of optimization matrix")
parser.add_argument('-r', '--res', type=int, default=1,
                    help="Resolution for optimization simulations")
parser.add_argument('-p', '--processes', type=int, default=None,
                    help="Number of worker processes to spawn")
args = parser.parse_args()

dim = args.dim
resolution = args.res
nproc = args.processes
design_yr = (4, 24)
focus_yr = (4, -24)
use_filter = False
box_sy = 1
box_sx = 0.5
n_lo = 1.1
n_hi = 1.2


def worker(M):
    bsw = BSWFocus(sim_resolution=resolution,
                   design_yr=design_yr,
                   focus_yr=focus_yr,
                   use_filter=use_filter,
                   n_lo=n_lo,
                   n_hi=n_hi,
                   box_sx=box_sx,
                   box_sy=box_sy)
    bsw.set_design(M)
    bsw.run()
    field = bsw.get_focus_box_field()
    return np.square(np.linalg.norm(field))


def optimize():
    Ml = np.zeros((int(dim / 2), dim))
    margin = 2
    margin_counter = 0
    max_field = 0
    field_list = [0]
    M_list = []
    Ml_bak = None
    first_neg = True
    t = []
    iterations = 0
    while True:
        t.append(time.time())
        pool = Pool(processes=nproc)

        results = []
        for i, j in np.transpose(np.where(Ml == 0)):
            tMl = np.copy(Ml)
            tMl[i, j] = 1
            tM = np.vstack((tMl, np.flipud(tMl)))
            results.append((pool.apply_async(worker, args=(tM,)), i, j))
        pool.close()
        pool.join()
        res = np.array([(result.get(), int(i), int(j)) for result, i, j in results])

        if not res.any():
            if margin_counter > 0:
                Ml = Ml_bak
            break

        field = res[np.argmax(res, axis=0)[0]]

        iterations += 1
        print("Iteration {:<6d}, dE = {}".format(iterations, field[0] - max_field))

        if field[0] < max_field:
            margin_counter += 1
            if first_neg:
                Ml_bak = np.copy(Ml)
                first_neg = False
        else:
            max_field = field[0]
            field_list.append(max_field)
            M_list.append(np.vstack((Ml, np.flipud(Ml))))
            margin_counter = 0
            first_neg = True

        if margin_counter <= margin:
            Ml[int(field[1]), int(field[2])] = 1
        else:
            Ml = Ml_bak
            break

    print("Optimization finished in {} iterations.".format(iterations))
    return np.array(M_list), np.array(field_list), np.array(t)


if __name__ == '__main__':
    fname = dt.strftime(dt.now(), '%Y%m%d-%H%M%S')
    m, e, t = optimize()
    bsw = BSWFocus(sim_resolution=resolution,
                   design_yr=design_yr,
                   focus_yr=focus_yr,
                   use_filter=use_filter,
                   n_lo=n_lo,
                   n_hi=n_hi,
                   box_sx=box_sx,
                   box_sy=box_sy)
    h5f = h5py.File('./run/{}_bsw_{}x{}_res{}.h5'.format(fname, dim, dim, resolution), 'w')
    h5f.create_dataset('design', data=m)
    h5f.create_dataset('focus', data=e)
    h5f.create_dataset('it_time', data=t)
    simgrp = h5f.create_group('sim')
    for key, value in bsw.to_dict().items():
        simgrp.create_dataset(key, data=value)
    h5f.close()

