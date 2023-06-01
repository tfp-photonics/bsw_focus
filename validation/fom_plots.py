#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
import h5py
import numpy as np
import matplotlib as mpl
mpl.use("pgf")
import matplotlib.pyplot as plt
from matplotlib import rc

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

names = [
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-102632_bsw_20x5_res5.h5',
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-102934_bsw_24x6_res5.h5',
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-103333_bsw_28x7_res5.h5',
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-103923_bsw_32x8_res5.h5',
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-104802_bsw_36x9_res5.h5',
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-105802_bsw_40x10_res5.h5',
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-110117_bsw_44x11_res5.h5',
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-112642_bsw_48x12_res5.h5',
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-120316_bsw_52x13_res5.h5',
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-125211_bsw_56x14_res5.h5',
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-125221_bsw_60x15_res5.h5',
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-135927_bsw_68x17_res5.h5',
    '/Users/yannick/Desktop/rebuttal/5um_sims/20180726-161735_bsw_80x20_res5.h5',
]

lbsw = 1.5555 / 1.1
feat = np.array([2.0, 1.6667, 1.4286, 1.25, 1.1111, 1.0, 0.9091, 0.8333,
                 0.7692, 0.7143, 0.6667, 0.5882, 0.5])

foms = []
for name in names:
    h5f = h5py.File(name, 'r')
    foms.append(list(h5f['focus']))
    h5f.close()

fig, ax = plt.subplots(1, 2, figsize=(8, 4))

for axi in ax:
    for tick in axi.xaxis.get_major_ticks():
        tick.label.set_fontsize(8)
    for tick in axi.yaxis.get_major_ticks():
        tick.label.set_fontsize(8)

for idx in [0, 5, 10, 12]:
    # grid = re.search('(\d+)x(\d+)', names[idx]).group(0)
    ax[0].plot(foms[idx], label=r'{:.2f} μm'.format(feat[idx]))

ax[0].set_xlim([0, len(foms[-1])])
ax[0].set_ylim([0, max(foms[-1])])
ax[0].set_xticks(range(0, 400, 50))
ax[0].set_xticklabels([r'{}'.format(int(x)) for x in range(0, 400, 50)])
ax[0].set_yticks(range(0, 40, 5))
ax[0].set_yticklabels([r'{}'.format(x) for x in range(0, 40, 5)])
ax[0].set_title(r'\textbf{(a)}', fontsize=12, loc='left')
ax[0].set_xlabel(r'Iterations', fontsize=8)
ax[0].set_ylabel(r'FOM (a.u.)', fontsize=8)
legend = ax[0].legend(loc='lower right', title=r'Feature size:',
                      frameon=True, framealpha=1.0,
                      prop={'size': 8})
plt.setp(legend.get_title(), fontsize=8)
ax[0].grid()

ax[1].plot([len(fom) for fom in foms], zorder=1)
ax[1].scatter(range(len(foms)), [len(fom) for fom in foms], c='k', marker='x',
              lw=0.8, zorder=2)
ax[1].set_xlim([min(feat), max(feat)])
ax[1].set_ylim([0, len(foms[-1])])
ax[1].set_xticks(range(0, len(foms), 2))
ax[1].set_xticklabels([r'{:.2f}'.format(x) for x in feat[0:14:2]])
ax[1].set_yticks(range(0, 400, 50))
ax[1].set_yticklabels([r'{}'.format(int(x)) for x in range(0, 400, 50)])
ax[1].set_title(r'\textbf{(b)}', fontsize=12, loc='left')
ax[1].set_xlabel(r'Feature size (μm)', fontsize=8)
ax[1].set_ylabel(r'Iterations', fontsize=8)
ax[1].grid()
plt.tight_layout()

plt.savefig('fom_evolution.png', bbox_inches='tight', dpi=300)
