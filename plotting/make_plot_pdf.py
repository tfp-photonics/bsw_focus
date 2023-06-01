#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import h5py
import argparse
import meep as mp
import numpy as np
from datetime import datetime
from ..util.bswfocus import BSWFocus
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import gridspec, colorbar
from matplotlib.colors import PowerNorm
import matplotlib.pyplot as plt


def main(args):
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{siunitx} \usepackage{physics}')
    dtname = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
    pdf = PdfPages('./{}_plots.pdf'.format(dtname))

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
        fnames.append(os.path.splitext(os.path.basename(fname))[0])
        bsw.run()

        eps = bsw.sim.get_array(center=mp.Vector3(0, 0),
                                size=mp.Vector3(bsw.sx, bsw.sy),
                                component=mp.Dielectric)
        epsilons.append(eps)
        ex = bsw.sim.get_array(center=mp.Vector3(0, 0),
                               size=mp.Vector3(bsw.sx, bsw.sy),
                               component=mp.Ex)
        ey = bsw.sim.get_array(center=mp.Vector3(0, 0),
                               size=mp.Vector3(bsw.sx, bsw.sy),
                               component=mp.Ey)
        fields.append(np.sqrt(np.square(np.abs(ex)) + np.square(np.abs(ey))))

    fields = [fields[i:i + 2] for i in range(0, len(fields), 2)]
    epsilons = [epsilons[i:i + 2] for i in range(0, len(epsilons), 2)]
    fnames = [fnames[i:i + 2] for i in range(0, len(fnames), 2)]
    for page in zip(epsilons, fields, fnames):
        fig, axes = plt.subplots(nrows=2, ncols=1, dpi=300, sharey=True, figsize=(8.27, 11.69))
        for row, big_ax in enumerate(axes, start=1):
            fn = page[2][row // 2]
            big_ax.set_title(r'{}'.format(fn.replace('_', '\_')), fontsize=14, y=1.01)
            big_ax.tick_params(labelcolor=(1., 1., 1., 0.), top=False, bottom=False, left=False, right=False)
            big_ax._frameon = False
        for ii in range(1, 5):
            eps = page[0][ii // 3]
            field = page[1][ii // 3]
            ax = fig.add_subplot(2, 2, ii)
            ax.set_xlim(0, field.shape[0])
            ax.set_xticks(np.linspace(0, field.shape[0], 5))
            ax.set_yticks(np.linspace(field.shape[1], 0, 6))
            ax.set_xticklabels(np.linspace(-(field.shape[0] - 1) / (2 * res), (field.shape[0] - 1) / (2 * res), 5, dtype=int))
            ax.set_yticklabels(np.linspace(0, (field.shape[1] - 2) / res, 6, dtype=int))
            ax.set_xlabel(r'x-axis (\SI{}{\micro\meter})', fontsize=10)
            ax.set_ylabel(r'z-axis (\SI{}{\micro\meter})', fontsize=10)
            if ii % 2:
                ax.imshow(eps.transpose(), interpolation='none', cmap='binary')
            else:
                plt.imshow(field.transpose(),
                           aspect='equal',
                           interpolation='none',
                           # norm=PowerNorm(0.6, vmin=field.min(), vmax=field.max()),
                           cmap='hot')
        fig.set_facecolor('w')
        plt.savefig(pdf, format='pdf')
        plt.close()
    pdf.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, nargs='+', required=True,
                        help="Input file(s)")
    args = parser.parse_args()
    main(args)
