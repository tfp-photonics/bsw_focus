#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('./tilt_results.txt', skiprows=1, unpack=False).T

fig, ax1 = plt.subplots()

lns1 = ax1.plot(data[0], data[1], 'r', label='fwhm')

ax2 = ax1.twinx()
lns2 = ax2.plot(data[0], data[2], 'g', label='intensity')
# plt.plot(data[0], data[3], label='focus distance')
# plt.plot(data[0], data[4], label='center')

ax1.set_xlabel('tilt (deg)')
ax1.set_ylabel('fwhm (nm)')
ax2.set_ylabel('intensity (a.u.)')

lns = lns1+lns2
labs = [l.get_label() for l in lns]
ax1.legend(lns, labs, loc='upper center')

plt.tight_layout()

