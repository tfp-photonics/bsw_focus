#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

foc_dist = [5.15, 5.05, 5.10, 5.20, 5.15, 5.00,
            5.05, 5.00, 4.90, 4.90, 4.85, 4.90, 4.90]
feat_size = [2.0,
             1.6666666666666667,
             1.4285714285714286,
             1.25,
             1.1111111111111112,
             1.0,
             0.9090909090909091,
             0.8333333333333334,
             0.7692307692307693,
             0.7142857142857143,
             0.6666666666666666,
             0.5882352941176471,
             0.5,
             ]

plt.scatter(feat_size, foc_dist, c='k', marker='x', lw=0.6, s=10, zorder=2)
plt.plot(feat_size, foc_dist, 'b--', lw=0.7, zorder=1)
plt.xlabel(r'Feature size ($\lambda_{\text{BSW}}$)', fontsize=10)
plt.ylabel(r'Focus distance (μm)')
plt.grid(linestyle='--', linewidth=0.5)
plt.savefig('test.png', bbox_inches='tight', dpi=300)
