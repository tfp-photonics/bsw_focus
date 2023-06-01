#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import h5py
import numpy as np
import matplotlib as mpl
mpl.use("pgf")
from matplotlib.gridspec import GridSpec
from matplotlib import patches
import matplotlib.pyplot as plt
from scipy.ndimage import rotate

mpl.rc('text', usetex=True)
mpl.rc('text.latex', preamble=r'\usepackage{cmbright}')
mpl.rc({'legend.fontsize': 8})

pgf_with_custom_preamble = {
    'font.family': 'sans-serif',
    # 'font.sans-serif': 'Helvetica Neue',
    'font.sans-serif': 'Arial',
    'text.usetex': True,
    'pgf.rcfonts': True,
    'pgf.preamble': [
        r'\usepackage[utf8]{inputenc}',
        r'\usepackage{amsmath}',
        r'\usepackage{siunitx}',
        r'\usepackage{physics}',
        r'\usepackage{unicode-math}',
        # r'\usepackage{fontspec}',
        # r'\setmainfont{Helvetica Neue}',
        # r'\setmathfont{Helvetica Neue}',
    ]
}
mpl.rcParams.update(pgf_with_custom_preamble)

info = '/Users/yannick/Desktop/rebuttal/results/gauss_beam.txt'
names = [
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma01_fields.h5',
    '/Users/yannick/Desktop/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma02_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma03_fields.h5',
    '/Users/yannick/Desktop/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma04_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma05_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma06_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma07_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma08_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma09_fields.h5',
    '/Users/yannick/Desktop/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma10_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma11_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma12_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma13_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma14_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma15_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma16_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma17_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma18_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma19_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma20_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma21_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma22_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma23_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma24_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma25_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma26_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma27_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma28_fields.h5',
    # '/home/yannick/data/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma29_fields.h5',
    '/Users/yannick/Desktop/rebuttal/gauss_beam/20180726-125221_bsw_60x15_res5_sigma30_fields.h5',
]

fields = []
eps = []
for name in names:
    h5f = h5py.File(name, 'r')
    ex = np.asarray(h5f['Ex']).T
    ey = np.asarray(h5f['Ey']).T
    ep = np.asarray(h5f['Dielectric']).T
    h5f.close()
    field = np.square(np.abs(ex)) + np.square(np.abs(ey))
    fields.append(field[200:, :])
    ep = np.ma.masked_where(ep < np.mean(ep), ep)
    eps.append(ep[200:, :])

gs1 = GridSpec(2, 2)
gs1.update(left=0.07, right=0.54, top=0.86, bottom=0.14, wspace=0.2, hspace=0.00)
ax1 = plt.subplot(gs1[0, 0])
ax2 = plt.subplot(gs1[0, 1])
ax3 = plt.subplot(gs1[1, 0])
ax4 = plt.subplot(gs1[1, 1])

gs2 = GridSpec(1, 1)
gs2.update(left=0.65, right=0.92, top=0.75, bottom=0.25, wspace=0.0, hspace=0.0)
ax5 = plt.subplot(gs2[0])

ax1.plot(40, 40, 'o',
         markeredgewidth=0.5,
         markeredgecolor='w',
         markerfacecolor='b')
ax1.imshow(fields[0], cmap='hot')
ax1.imshow(eps[0], cmap='summer', alpha=0.6)
ax1.set_ylabel(r'z-axis (μm)', fontsize=8)
ax1.set_yticks(np.linspace(fields[0].shape[0], 0, 3))
ax1.set_yticklabels([str(x) for x in np.linspace(0,
                                                 (fields[0].shape[0] - 2) / 20,
                                                 3, dtype=int)])
ax1.set_xticks([], [])
ax1.set_title(r'\textbf{(a)}', fontsize=12, loc='left')


ax2.plot(40, 40, 'D',
         markersize=5,
         markeredgewidth=0.5,
         markeredgecolor='w',
         markerfacecolor='b')
ax2.imshow(fields[1], cmap='hot')
ax2.imshow(eps[1], cmap='summer', alpha=0.6)
ax2.set_xticks([], [])
ax2.set_yticks([], [])
ax2.set_title(r'\textbf{(b)}', fontsize=12, loc='left')


ax3.plot(40, 40, '^',
         markeredgewidth=0.5,
         markeredgecolor='w',
         markerfacecolor='b')
ax3.imshow(fields[2], cmap='hot')
ax3.imshow(eps[2], cmap='summer', alpha=0.6)
ax3.set_xlabel(r'x-axis (μm)', fontsize=8)
ax3.set_ylabel(r'z-axis (μm)', fontsize=8)
ax3.set_xticks(np.linspace(0, fields[2].shape[1], 5))
ax3.set_yticks(np.linspace(fields[0].shape[0], 0, 3))
ax3.set_yticklabels([str(x) for x in np.linspace(0,
                                                 (fields[0].shape[0] - 2) / 20,
                                                 3, dtype=int)])
ax3.set_xticklabels([str(x) for x in np.linspace(-(fields[2].shape[1] - 1) / 40,
                                                 (fields[2].shape[1] - 1) / 40,
                                                 5, dtype=int)])
ax3.set_title(r'\textbf{(c)}', fontsize=12, loc='left')


ax4.plot(40, 40, '*',
         markersize=8,
         markeredgewidth=0.5,
         markeredgecolor='w',
         markerfacecolor='b')
ax4.imshow(fields[3], cmap='hot')
ax4.imshow(eps[3], cmap='summer', alpha=0.6)
ax4.set_xlabel(r'x-axis (μm)', fontsize=8)
ax4.set_xticks(np.linspace(0, fields[3].shape[1], 5))
ax4.set_xticklabels([str(x) for x in np.linspace(-(fields[2].shape[1] - 1) / 40,
                                                 (fields[2].shape[1] - 1) / 40,
                                                 5, dtype=int)])
ax4.set_yticks([], [])
ax4.set_title(r'\textbf{(d)}', fontsize=12, loc='left')


data = []
with open(info, 'r') as f:
    f.readline()
    for line in f:
        elements = line.split()
        data.append([
            int(re.search('(?:sigma)(\d+)', elements[0]).group(1)),
            float(elements[1]),
            float(elements[3]),
        ])
data = np.array(data[1:])

lbsw = 1.5555 / 1.1
data[:, 1] /= lbsw

tilt = np.ma.array(data[:, 0], mask=False)
fwhm = np.ma.array(data[:, 1], mask=False)
ints = np.ma.array(data[:, 2], mask=False)

ax5.plot(tilt, ints, 'g--', lw=0.7, zorder=1)
ax5.set_ylim([0, 4.5])
ax5.set_yticks([0, 1, 2, 3, 4])
ax5.set_yticklabels([str(x) for x in [0, 1, 2, 3, 4]])
ax5.set_ylabel(r'Intensity (a.u.)', color='g', fontsize=8)

ax6 = ax5.twinx()
ax6.plot(tilt, fwhm, 'r--', lw=0.7, zorder=1)
# ax6.plot([-1, 31], [0.708 / lbsw, 0.708 / lbsw], 'k--', lw=0.7, zorder=1)
ax6.set_ylim([0, 1.6])
ax6.set_yticks([0.0, 0.3, 0.708 / lbsw, 0.6, 0.9, 1.2, 1.5])
ax6.set_yticklabels(['{:.1f}'.format(x) for x in [0.0, 0.3, 0.708 / lbsw, 0.6, 0.9, 1.2, 1.5]], fontsize=8)
ax6.set_ylabel(r'FWHM ($\lambda_{\text{BSW}}$)', fontsize=8, color='r')

ax6.add_patch(patches.Ellipse(
    (25, 0.52),
    3.5,
    0.11,
    facecolor='w',
    edgecolor='r',
    angle=0,
    zorder=2,
    linewidth=0.3,
    fill=False
))

ax6.add_patch(patches.Ellipse(
    (4, 0.35),
    3.5,
    0.11,
    facecolor='w',
    edgecolor='g',
    angle=0,
    zorder=2,
    linewidth=0.3,
    fill=False
))

ax6.arrow(27, 0.56, 2.6, 0.09, linewidth=0.5,
          head_width=0.02, head_length=0.7, fc='r', ec='r', zorder=2)
ax6.arrow(2.4, 0.40, -1.2, 0.05, linewidth=0.5,
          head_width=0.02, head_length=0.7, fc='g', ec='g', zorder=2)

idx = [0, 2, 8, 28]
fwhm.mask[idx] = True
ints.mask[idx] = True
ax6.scatter(tilt, fwhm, c='k', marker='x', lw=0.6, s=10, zorder=2)
ax5.scatter(tilt, ints, c='k', marker='x', lw=0.6, s=10, zorder=2)

fwhm.mask[idx] = False
ints.mask[idx] = False
ax5.scatter(tilt[idx[0]], ints[idx[0]], c='b', marker='o', lw=0.0, s=30, zorder=2)
ax5.scatter(tilt[idx[1]], ints[idx[1]], c='b', marker='D', lw=0.0, s=20, zorder=2)
ax5.scatter(tilt[idx[2]], ints[idx[2]], c='b', marker='^', lw=0.0, s=30, zorder=2)
ax5.scatter(tilt[idx[3]], ints[idx[3]], c='b', marker='*', lw=0.0, s=40, zorder=2)
ax6.scatter(tilt[idx[0]], fwhm[idx[0]], c='b', marker='o', lw=0.0, s=30, zorder=2)
ax6.scatter(tilt[idx[1]], fwhm[idx[1]], c='b', marker='D', lw=0.0, s=20, zorder=2)
ax6.scatter(tilt[idx[2]], fwhm[idx[2]], c='b', marker='^', lw=0.0, s=30, zorder=2)
ax6.scatter(tilt[idx[3]], fwhm[idx[3]], c='b', marker='*', lw=0.0, s=40, zorder=2)

# ax5.set_xlim([max(feat), min(feat)])
# ax5.set_xlim([min(feat), max(feat)])
ax5.set_xlim([0, 31])
ax5.set_xticks([0, 5, 10, 15, 20, 25, 30])
ax5.set_xticklabels([str(x) for x in [0, 5, 10, 15, 20, 25, 30]], fontsize=8)
ax5.set_title(r'\textbf{(e)}', fontsize=12, loc='left')
ax5.set_xlabel(r'Beam waist diameter (μm)', fontsize=8)
ax5.tick_params('y', colors='g')
ax5.xaxis.grid(linestyle='--', linewidth=0.5)
ax6.yaxis.grid(linestyle='--', linewidth=0.5)
ax6.tick_params('y', colors='r')

for axi in [ax1, ax2, ax3, ax4, ax5, ax6]:
    for tick in axi.xaxis.get_major_ticks():
        tick.label.set_fontsize(8)
    for tick in axi.yaxis.get_major_ticks():
        tick.label.set_fontsize(8)


plt.savefig('gauss_beam.png', bbox_inches='tight', dpi=300)
