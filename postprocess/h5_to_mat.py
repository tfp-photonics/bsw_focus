#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import h5py
import numpy as np
from scipy.io import loadmat, savemat


names = [
    ['20180403-045219_bsw_60x30', 's3'],
    ['20180403-013101_bsw_60x15', 's0'],
    ['20180403-135045_bsw_60x15', 'u2'],
    ['20180403-172333_bsw_60x30', 'u5'],
    ['20180326-192008_bsw_10x10', 'l0'],
    ['20180326-192057_bsw_20x20', 'l1'],
    ['20180326-192852_bsw_30x30', 'l2'],
    ['20180326-201350_bsw_40x40', 'l3'],
    ['20180403-115828_bsw_6x12', 's4'],
    ['20180327-021417_bsw_10x10', 'm8'],
    ['20180402-230449_bsw_6x12', 'q8'],
]

for name, idx in names:
    h5f = h5py.File('/scratch/local/data/fields/{}_res5_fields.h5'.format(name), 'r')
    sim_ex = np.flipud(np.asarray(h5f['Ex']).T)
    sim_ey = np.flipud(np.asarray(h5f['Ey']).T)
    sim_hz = np.flipud(np.asarray(h5f['Hz']).T)
    sim_eps = np.flipud(np.asarray(h5f['Dielectric']).T)
    h5f.close()

    output_dict = {
        'Ex': sim_ex,
        'Ey': sim_ey,
        'Hz': sim_hz,
        'Dielectric': sim_eps,
    }

    mat = savemat('/scratch/local/data/matlab/{}_sim.mat'.format(idx), output_dict)
