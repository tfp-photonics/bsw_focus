#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import h5py
import numpy as np
from scipy.io import loadmat


mat = loadmat('/scratch/local/data/snom/S4.mat')
h5f = h5py.File('/scratch/local/data/snom/s4_snom.h5', 'w')
h5f['intensity'] = np.flipud(mat['S4_AMP'])
h5f['intensity_close'] = np.flipud(mat['S4_AMP_CloseUp'])
h5f['phase'] = np.flipud(mat['S4_Phase'])
h5f['phase_close'] = np.flipud(mat['S4_Phase_CloseUp'])
h5f.close()


