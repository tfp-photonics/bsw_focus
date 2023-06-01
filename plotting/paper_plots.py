#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import h5py
import numpy as np
import matplotlib as mpl
mpl.use("pgf")
from matplotlib.gridspec import GridSpec
from matplotlib import patches
import matplotlib.pyplot as plt

pgf_with_custom_preamble = {
    'font.family': 'sans-serif',
    'font.sans-serif': 'Helvetica Neue',
    # 'font.sans-serif': 'Arial',
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

# info = '/Users/yannick/Downloads/paper_data/1um/info_plots/info.txt'
# names = [
#     '/Users/yannick/Downloads/paper_data/1um/fields/20180727-130240_bsw_20x5_res5_fields.h5',
#     '/Users/yannick/Downloads/paper_data/1um/fields/20180727-133254_bsw_40x10_res5_fields.h5',
#     '/Users/yannick/Downloads/paper_data/1um/fields/20180727-163634_bsw_60x15_res5_fields.h5',
#     '/Users/yannick/Downloads/paper_data/1um/fields/20180727-200253_bsw_80x20_res5_fields.h5',
# ]

info = '/Users/yannick/Downloads/paper_data/5um/info_plots/info.txt'
names = [
    '/Users/yannick/Downloads/paper_data/5um/fields/20180726-102632_bsw_20x5_res5_fields.h5',
    '/Users/yannick/Downloads/paper_data/5um/fields/20180726-105802_bsw_40x10_res5_fields.h5',
    '/Users/yannick/Downloads/paper_data/5um/fields/20180726-125221_bsw_60x15_res5_fields.h5',
    '/Users/yannick/Downloads/paper_data/5um/fields/20180726-161735_bsw_80x20_res5_fields.h5',
]

fields = []
eps = []
for name in names:
    h5f = h5py.File(name, 'r')
    ex = np.asarray(h5f['Ex']).T
    ey = np.asarray(h5f['Ey']).T
    ep = np.asarray(h5f['Dielectric']).T
    h5f.close()
    fields.append(np.square(np.abs(ex)) + np.square(np.abs(ey)))
    eps.append(np.ma.masked_where(ep < np.mean(ep), ep))


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
ax1.set_ylabel(r'z-axis (μm)', fontsize=10)
ax1.set_yticks(np.linspace(fields[0].shape[1], 0, 5))
ax1.set_yticklabels([str(x) for x in np.linspace(0,
                                                 (fields[0].shape[1] - 2) / 20,
                                                 5, dtype=int)])
ax1.set_xticks([], [])
ax1.set_title(r'\textbf{(a)}', fontsize=14, loc='left')


ax2.plot(40, 40, 'D',
         markersize=5,
         markeredgewidth=0.5,
         markeredgecolor='w',
         markerfacecolor='b')
ax2.imshow(fields[1], cmap='hot')
ax2.imshow(eps[1], cmap='summer', alpha=0.6)
ax2.set_xticks([], [])
ax2.set_yticks([], [])
ax2.set_title(r'\textbf{(b)}', fontsize=14, loc='left')


ax3.plot(40, 40, '^',
         markeredgewidth=0.5,
         markeredgecolor='w',
         markerfacecolor='b')
ax3.imshow(fields[2], cmap='hot')
ax3.imshow(eps[2], cmap='summer', alpha=0.6)
ax3.set_xlabel(r'x-axis (μm)', fontsize=10)
ax3.set_ylabel(r'z-axis (μm)', fontsize=10)
ax3.set_xticks(np.linspace(0, fields[2].shape[0], 5))
ax3.set_yticks(np.linspace(fields[2].shape[1], 0, 5))
ax3.set_yticklabels([str(x) for x in np.linspace(0,
                                                 (fields[0].shape[1] - 2) / 20,
                                                 5, dtype=int)])
ax3.set_xticklabels([str(x) for x in np.linspace(-(fields[2].shape[0] - 1) / 40,
                                                 (fields[2].shape[0] - 1) / 40,
                                                 5, dtype=int)])
ax3.set_title(r'\textbf{(c)}', fontsize=14, loc='left')


ax4.plot(40, 40, '*',
         markersize=8,
         markeredgewidth=0.5,
         markeredgecolor='w',
         markerfacecolor='b')
ax4.imshow(fields[3], cmap='hot')
ax4.imshow(eps[3], cmap='summer', alpha=0.6)
ax4.set_xlabel(r'x-axis (μm)', fontsize=10)
ax4.set_xticks(np.linspace(0, fields[3].shape[0], 5))
ax4.set_xticklabels([str(x) for x in np.linspace(-(fields[2].shape[0] - 1) / 40,
                                                 (fields[2].shape[0] - 1) / 40,
                                                 5, dtype=int)])
ax4.set_yticks([], [])
ax4.set_title(r'\textbf{(d)}', fontsize=14, loc='left')



data = []
with open(info, 'r') as f:
    f.readline()
    for line in f:
        elements = line.split()
        data.append([
            float(elements[3]),
            float(elements[4]),
            float(elements[6]),
        ])

data = np.array(data)
data = data[data[:, 0].argsort()[::-1]]

lbsw = 1.5555 / 1.1
data[:, 0] /= lbsw
data[:, 1] /= lbsw

feat = np.ma.array(data[:, 0], mask=False)
fwhm = np.ma.array(data[:, 1], mask=False)
ints = np.ma.array(data[:, 2], mask=False)

ax5.plot(feat, ints, 'g--', lw=0.7, zorder=1)
ax5.set_yticks([2, 3, 4, 5])
ax5.set_yticklabels([str(x) for x in [2, 3, 4, 5]])
ax5.set_ylabel(r'Intensity (a.u.)', color='g')

ax6 = ax5.twinx()
ax6.plot(feat, fwhm, 'r--', lw=0.7, zorder=1)
ax6.set_yticks([0.50, 0.55, 0.60, 0.65, 0.70, 0.75])
ax6.set_yticklabels(['{:.2f}'.format(x) for x in [0.50, 0.55, 0.60, 0.65, 0.70, 0.75]])
ax6.set_ylabel(r'FWHM ($\lambda_{\text{BSW}}$)', fontsize=10, color='r')

ax6.add_patch(patches.Ellipse(
    (1.225, 0.65),
    0.20,
    0.035,
    facecolor='w',
    edgecolor='r',
    angle=0,
    zorder=2,
    linewidth=0.3,
    fill=False
))

ax6.add_patch(patches.Ellipse(
    (0.65, 0.65),
    0.20,
    0.035,
    facecolor='w',
    edgecolor='g',
    angle=0,
    zorder=2,
    linewidth=0.3,
    fill=False
))

ax6.arrow(1.35, 0.64, 0.07, -0.006, linewidth=0.5,
          head_width=0.006, head_length=0.025, fc='r', ec='r', zorder=2)
ax6.arrow(0.47, 0.65, -0.15, 0.0, linewidth=0.5,
          head_width=0.006, head_length=0.025, fc='g', ec='g', zorder=2)

idx = [0, 5, 10, 12]
fwhm.mask[idx] = True
ints.mask[idx] = True
ax6.scatter(feat, fwhm, c='k', marker='x', lw=0.6, s=10, zorder=2)
ax5.scatter(feat, ints, c='k', marker='x', lw=0.6, s=10, zorder=2)

fwhm.mask[idx] = False
ints.mask[idx] = False
ax5.scatter(feat[idx[0]], ints[idx[0]], c='b', marker='o', lw=0.0, s=30, zorder=2)
ax5.scatter(feat[idx[1]], ints[idx[1]], c='b', marker='D', lw=0.0, s=20, zorder=2)
ax5.scatter(feat[idx[2]], ints[idx[2]], c='b', marker='^', lw=0.0, s=30, zorder=2)
ax5.scatter(feat[idx[3]], ints[idx[3]], c='b', marker='*', lw=0.0, s=40, zorder=2)
ax6.scatter(feat[idx[0]], fwhm[idx[0]], c='b', marker='o', lw=0.0, s=30, zorder=2)
ax6.scatter(feat[idx[1]], fwhm[idx[1]], c='b', marker='D', lw=0.0, s=20, zorder=2)
ax6.scatter(feat[idx[2]], fwhm[idx[2]], c='b', marker='^', lw=0.0, s=30, zorder=2)
ax6.scatter(feat[idx[3]], fwhm[idx[3]], c='b', marker='*', lw=0.0, s=40, zorder=2)

# ax5.set_xlim([max(feat), min(feat)])
# ax5.set_xlim([min(feat), max(feat)])
ax5.set_xlim([0.25, 1.50])
ax5.set_xticks([1.5, 1.25, 1.0, 0.75, 0.5, 0.25])
ax5.set_xticklabels([str(x) for x in [1.5, 1.25, 1.0, 0.75, 0.5, 0.25]])
ax5.set_title(r'\textbf{(e)}', fontsize=14, loc='left')
ax5.set_xlabel(r'Feature size ($\lambda_{\text{BSW}}$)', fontsize=10)
ax5.tick_params('y', colors='g')
ax5.xaxis.grid(linestyle='--', linewidth=0.5)
ax6.yaxis.grid(linestyle='--', linewidth=0.5)
ax6.tick_params('y', colors='r')

plt.savefig('figure_2.pdf', bbox_inches='tight', dpi=300)
