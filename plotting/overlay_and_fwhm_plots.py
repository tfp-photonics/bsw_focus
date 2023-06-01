#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import h5py
import argparse
import numpy as np
from ..util.bswfocus import BSWFocus
from ..util.plotter import *
from ..util.geometry import make_isosceles


def overlay_plots(bsw, fname, savefig=''):
    xall, yall, fx, fy, spline, yloc = bsw.get_focus_fwhm(sx=3)
    roots = spline.roots()
    middle = float(len(roots)) / 2.
    r1, r2 = roots[int(middle - 0.5)], roots[int(middle + 0.5)]
    fwhm = np.abs(r2 - r1)
    x = np.linspace(np.min(fx), np.max(fx), 100)
    y = spline(x)
    y += np.max(fy) / 2

    feature_size = np.sum(np.abs(bsw.design_xr)) / bsw.design_matrix.shape[0]

    eps = bsw.sim.get_array(center=mp.Vector3(0, 5),
                            size=mp.Vector3(bsw.sx, bsw.sy - 10),
                            component=mp.Dielectric)
    ex = bsw.sim.get_array(center=mp.Vector3(0, 5),
                           size=mp.Vector3(bsw.sx, bsw.sy - 10),
                           component=mp.Ex)
    ey = bsw.sim.get_array(center=mp.Vector3(0, 5),
                           size=mp.Vector3(bsw.sx, bsw.sy - 10),
                           component=mp.Ey)

    field = np.square(np.abs(ex)) + np.square(np.abs(ey))
    eps = np.ma.masked_where(eps < np.mean(eps), eps)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rc('text.latex', preamble=r'\usepackage{amsmath}'
           r'\usepackage{siunitx}'
           r'\usepackage{physics}')

    fig, ax = plt.subplots(1, 1, dpi=200)

    ax.imshow(field.T, cmap='hot', interpolation='none')
    ax.imshow(eps.T, cmap='summer', interpolation='none', alpha=0.4)
    ax.set_xlabel(r'x-axis (\SI{}{\micro\meter})', fontsize=10)
    ax.set_ylabel(r'z-axis (\SI{}{\micro\meter})', fontsize=10)

    ax.set_xticks(np.linspace(0, field.shape[0], 5))
    ax.set_yticks(np.linspace(field.shape[1], 0, 5))
    ax.set_xticklabels(np.linspace(-(field.shape[0] - 1) / (2 * bsw.sim.resolution),
                                   (field.shape[0] - 1) / (2 * bsw.sim.resolution),
                                   5, dtype=int))
    ax.set_yticklabels(np.linspace(0, (field.shape[1] - 2) / bsw.sim.resolution,
                                   5, dtype=int))

    plt.title(r'Feature size: \SI{{{:.2f}}}{{\micro\meter}}, '
              r'FWHM: \SI{{{:.2f}}}{{\micro\meter}}'.format(feature_size,
                                                            fwhm), fontsize=12)
    plt.tight_layout()

    if savefig != '':
        plt.savefig('{}{}_res{}_overlay.png'.format(savefig, fname, bsw.sim.resolution),
                    dpi=300, bbox_inches='tight')
    else:
        plt.show()


def plot_focus(bsw, fit_method=None, sx=None, yr=None, interpolation='none', fname=None, savefig=''):
    dim = (0, 0) if bsw.design_matrix is None else bsw.design_matrix.shape
    res = bsw.sim.resolution
    if fname is None:
        fname = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S') + '_{}x{}'.format(dim[0], dim[1])

    if fit_method == 'gauss':
        fx, fy, fit = bsw.get_focus_intensity_fit(yr=yr, sx=sx)
        fwhm = fit.params['fwhm'].value
        x = np.linspace(np.min(fx), np.max(fx), 100)
        y = fit.eval(GaussianModel().make_params(**fit.best_values), x=x)
    else:
        xall, yall, fx, fy, spline, yloc = bsw.get_focus_fwhm(yr=yr, sx=sx)
        roots = spline.roots()
        middle = float(len(roots)) / 2.
        r1, r2 = roots[int(middle - 0.5)], roots[int(middle + 0.5)]
        fwhm = np.abs(r2 - r1)
        x = np.linspace(np.min(fx), np.max(fx), 100)
        y = spline(x)
        y += np.max(fy) / 2

    feature_size = np.sum(np.abs(bsw.design_xr)) / bsw.design_matrix.shape[0]

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{siunitx} \usepackage{physics}')
    fig, ax = plt.subplots(1, 1, dpi=300)
    ax.scatter(fx, fy, c='k', marker='x', label='Simulation')
    ax.plot(xall, yall, 'b-', lw=0.7, label='Intensity profile')
    ax.plot(x, y, 'r--', label='Fit')
    ax.plot((-fwhm / 2, fwhm / 2), (np.max(y) / 2, np.max(y) / 2), 'g',
            label='FWHM (\SI{{{:.2f}}}{{\micro\meter}})'.format(fwhm))
    ax.set_xlabel(r'x-axis (\SI{}{\micro\meter})', fontsize=10)
    ax.set_ylabel(r'$\abs{E_z}^2$ (a.u.)', fontsize=10)
    plt.legend(loc='best')
    plt.title(r'Feature size: \SI{{{:.2f}}}{{\micro\meter}}, '
              r'FWHM: \SI{{{:.2f}}}{{\micro\meter}}'.format(feature_size, fwhm), fontsize=12)
    ax.grid()

    if savefig != '':
        plt.savefig('{}{}_res{}_fwhm.png'.format(savefig, fname, bsw.sim.resolution),
                    dpi=300, bbox_inches='tight')
    else:
        plt.show()

    return fname, bsw.design_matrix.shape, feature_size, fwhm, yloc, np.max(y)


def main(args):
    info = []
    for fpath in args.file:
        h5f = h5py.File(fpath, 'r')
        d = {k: h5f['sim'][k].value for k in h5f['sim'].keys()}
        m = np.array(h5f['design'])
        h5f.close()

        d.update({
            'sim_resolution': args.res,
        })

        bsw = BSWFocus(**d)
        bsw.set_design(m[-1])

        fn = os.path.basename(fpath)
        basename = os.path.splitext(fn)[0]
        yr = (-25, np.max(bsw.focus_yr))

        bsw.run()

        overlay_plots(bsw, basename, savefig=args.save)
        fname, shape, feat, fwhm, yloc, intensity = plot_focus(bsw, sx=3, yr=yr,
                                                               fname=basename,
                                                               savefig=args.save)
        info.append([fname, shape[0], shape[1], feat, fwhm, bsw.design_yr[0] - yloc, intensity])

    with open('info.txt', 'w') as out:
        out.write('name sx, sy, feature_size, fwhm, foc_dist, intensity\n')
        for line in info:
            for element in line:
                out.write('{} '.format(element))
            out.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', type=str, default="", nargs='+',
                        help="Dataset file")
    parser.add_argument('-r', '--res', type=int, default=10,
                        help="Resolution for plotting simulation")
    parser.add_argument('-s', '--save', type=str, default='',
                        help="Save plots")
    args = parser.parse_args()
    main(args)
