#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import meep as mp
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec, colorbar
from lmfit.models import GaussianModel
from datetime import datetime


def plot_with_eps(bsw, xr=None, yr=None, interpolation='none', fname=None, savefig=''):
    cx = 0 if xr is None else np.mean(xr)
    cy = 0 if yr is None else np.mean(yr)
    sx = bsw.sx if xr is None else np.abs(xr[1] - xr[0])
    sy = bsw.sy if yr is None else np.abs(yr[1] - yr[0])
    dim = (0, 0) if bsw.design_matrix is None else bsw.design_matrix.shape
    res = bsw.sim.resolution
    if fname is None:
        fname = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S') + '_{}x{}'.format(dim[0], dim[1])

    eps = bsw.sim.get_array(center=mp.Vector3(cx, cy),
                            size=mp.Vector3(sx, sy),
                            component=mp.Dielectric)
    ex = bsw.sim.get_array(center=mp.Vector3(cx, cy),
                           size=mp.Vector3(sx, sy),
                           component=mp.Ex)
    ey = bsw.sim.get_array(center=mp.Vector3(cx, cy),
                           size=mp.Vector3(sx, sy),
                           component=mp.Ey)
    field = np.square(np.abs(ex)) + np.square(np.abs(ey))

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{siunitx} \usepackage{physics}')
    fig, ax = plt.subplots(1, 2, dpi=200, sharey=True)
    caxm = fig.add_axes([0.438, 0.11, 0.03, 0.77])
    ticksm = [round(np.min(eps), 2),
              round(np.max(eps), 2)]
    normm = plt.Normalize(ticksm[0], ticksm[-1])
    cbarm = colorbar.ColorbarBase(caxm, cmap='binary', orientation='vertical', norm=normm)
    cbarm.set_ticks(ticksm)
    cbarm.ax.set_yticklabels(ticksm)
    caxl = fig.add_axes([0.86, 0.11, 0.03, 0.77])
    ticksl = [round(np.min(field), 2),
              round(np.max(field) / 2, 2),
              round(np.max(field), 2)]
    norml = plt.Normalize(ticksl[0], ticksl[-1])
    cbarl = colorbar.ColorbarBase(caxl, cmap='jet', orientation='vertical', norm=norml)
    cbarl.set_ticks(ticksl)
    cbarl.ax.set_yticklabels(ticksl)
    medium = ax[0].imshow(eps.transpose(), interpolation=interpolation, cmap='binary', norm=normm)
    light = ax[1].imshow(field.transpose(),
                         aspect='equal',
                         interpolation=interpolation,
                         norm=norml,
                         cmap='jet')
    ax[0].set_ylabel(r'z-axis (\SI{}{\micro\meter})', fontsize=10)
    for axi in ax:
        axi.set_xticks(np.linspace(0, field.shape[0], 5))
        axi.set_yticks(np.linspace(field.shape[1], 0, 6))
        axi.set_xticklabels(np.linspace(-(field.shape[0] - 1) / (2 * res), (field.shape[0] - 1) / (2 * res), 5, dtype=int))
        axi.set_yticklabels(np.linspace(0, (field.shape[1] - 2) / res, 6, dtype=int))
        axi.set_xlabel(r'x-axis (\SI{}{\micro\meter})', fontsize=10)
    ax[0].set_title(r'Dielectric matrix', fontsize=12)
    ax[1].set_title(r'Electric field intensity', fontsize=12)
    plt.suptitle(r'2D optimization for ${}\times{}$ matrix'.format(dim[0], dim[1]), fontsize=14, y=1.01)
    if savefig != '':
        plt.savefig('{}{}_res{}_epsplot.png'.format(savefig, fname, res), bbox_inches='tight')
    else:
        plt.show()


def plot_intensities(bsw, xr=None, yr=None, interpolation='none', fname=None, savefig=''):
    dim = (0, 0) if bsw.design_matrix is None else bsw.design_matrix.shape
    if fname is None:
        fname = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S') + '_{}x{}'.format(dim[0], dim[1])
    if xr is None:
        xr = bsw.focus_xr
    if yr is None:
        yr = bsw.focus_yr
    cx = np.mean(xr)
    cy = np.mean(yr)
    sx = np.abs(xr[1] - xr[0])
    sy = np.abs(yr[1] - yr[0])
    res = bsw.sim.resolution

    field1 = bsw.sim.get_array(center=mp.Vector3(cx, cy),
                               size=mp.Vector3(sx, sy),
                               component=mp.Ex)
    field2 = bsw.sim.get_array(center=mp.Vector3(cx, cy),
                               size=mp.Vector3(sx, sy),
                               component=mp.Ey)
    field = (np.square(np.abs(field1)) + np.square(np.abs(field2))).T

    x = np.arange(field.shape[1])
    y = np.arange(field.shape[0])

    field_y1 = bsw.sim.get_array(center=mp.Vector3(cx, cy),
                                 size=mp.Vector3(0, sy),
                                 component=mp.Ex)
    field_y2 = bsw.sim.get_array(center=mp.Vector3(cx, cy),
                                 size=mp.Vector3(0, sy),
                                 component=mp.Ey)
    field_y = (np.square(np.abs(field_y1)) + np.square(np.abs(field_y2))).T
    yloc = bsw.get_focus_y(xr, yr, False)

    field_x1 = bsw.sim.get_array(center=mp.Vector3(cx, cy - yloc),
                                 size=mp.Vector3(sx, 0),
                                 component=mp.Ex)
    field_x2 = bsw.sim.get_array(center=mp.Vector3(cx, cy - yloc),
                                 size=mp.Vector3(sx, 0),
                                 component=mp.Ey)
    field_x = (np.square(np.abs(field_x1)) + np.square(np.abs(field_x2))).T
    savg_field_y = bsw.get_filter(field_y)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{siunitx} \usepackage{physics}')
    fig = plt.figure(dpi=200)
    gs = gridspec.GridSpec(2, 2, width_ratios=[2, 1], height_ratios=[1, 2])
    gs.update(wspace=0.06, hspace=0.06)
    ax = fig.add_subplot(gs[1, 0])
    axx = fig.add_subplot(gs[0, 0], sharex=ax)
    axy = fig.add_subplot(gs[1, 1], sharey=ax)
    ax.imshow(field, origin='lower', aspect='auto', cmap='jet')
    ax.scatter(np.mean(x), np.mean(y) - yloc * res, marker='x', c='red', s=50, label=r'focus')
    axx.plot(x, field.mean(0), label=r'$x_{\text{mean}}$')
    axx.plot(x, field_x, label=r'$x_0$')
    axy.plot(field.mean(1), y, label=r'$y_{\text{mean}}$')
    axy.plot(field_y, y, label=r'$y_{x_0}$')
    axy.plot(savg_field_y, y, label=r'$y_{\text{maxfilt}}$')
    ax.legend(fontsize=8)
    axx.legend(fontsize=8)
    axy.legend(fontsize=8)
    ax.set_xticks(np.linspace(0, sx * res, 5))
    ax.set_yticks(np.linspace(sy * res, 0, 5))
    ax.set_xticklabels(np.linspace(-sx / 2, sx / 2, 5, dtype=int))
    ax.set_yticklabels(np.linspace(0, sy, 5, dtype=int))
    ax.set_xlim((0, np.max(x)))
    ax.set_ylim((np.max(y), 0))
    ax.set_xlabel(r'x-axis (\SI{}{\micro\meter})', fontsize=10)
    ax.set_ylabel(r'z-axis (\SI{}{\micro\meter})', fontsize=10)
    axx.set_ylabel(r'$\abs{E_z}^2$', fontsize=10)
    axy.set_xlabel(r'$\abs{E_z}^2$', fontsize=10)
    axx.xaxis.set_ticks_position('none')
    axy.yaxis.set_ticks_position('none')
    axx.grid()
    axy.grid()
    plt.setp(axx.get_xticklabels(), visible=False)
    plt.setp(axy.get_yticklabels(), visible=False)
    plt.suptitle(r'Intensity distribution in optimization target space', fontsize=14)
    if savefig != '':
        plt.savefig('{}{}_res{}_intensity.png'.format(savefig, fname, bsw.sim.resolution), bbox_inches='tight')
    else:
        plt.show()


def plot_stats(e, t, fname=None, savefig=''):
    if fname is None:
        fname = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S') + '_{}x{}_res{}'.format(dim[0], dim[1])

    dt = np.diff(t)

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{siunitx} \usepackage{physics}')
    fig, ax = plt.subplots(2, 1, dpi=200, sharex=True)
    ax[0].plot(e)
    ax[1].plot(dt)
    plt.xlim((0, e.shape[0] - 1))
    ax[0].set_ylim((np.min(e), np.max(e)))
    ax[1].set_ylim((np.min(dt), np.max(dt)))
    ax[0].set_ylabel(r'$\abs{E_z}^2$', fontsize=10)
    ax[1].set_ylabel(r'seconds', fontsize=10)
    ax[0].set_title(r'Electric field intensity in focus box', fontsize=12)
    ax[1].set_title(r'Time per iteration (average: {:.2f}s)'.format(np.mean(dt)), fontsize=12)
    plt.xlabel(r'Iteration n', fontsize=10)
    plt.grid()
    if savefig != '':
        plt.savefig('{}{}_convergence.png'.format(savefig, fname), bbox_inches='tight')
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
        fx, fy, spline = bsw.get_focus_fwhm(yr=yr, sx=sx)
        roots = spline.roots()
        middle = float(len(roots)) / 2.
        r1, r2 = roots[int(middle - 0.5)], roots[int(middle + 0.5)]
        fwhm = np.abs(r2 - r1)
        x = np.linspace(np.min(fx), np.max(fx), 100)
        y = spline(x)
        y += np.max(fy) / 2

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{siunitx} \usepackage{physics}')
    fig, ax = plt.subplots(1, 1, dpi=200)
    ax.scatter(fx, fy, c='k', marker='x', label='Simulation')
    ax.plot(x, y, 'r--', label='Fit')
    ax.plot((-fwhm / 2, fwhm / 2), (np.max(y) / 2, np.max(y) / 2), 'g',
            label='FWHM (\SI{{{:.2f}}}{{\micro\meter}})'.format(fwhm))
    ax.set_xlabel(r'x-axis (\SI{}{\micro\meter})', fontsize=10)
    ax.set_ylabel(r'$\abs{E_z}^2$', fontsize=10)
    plt.legend(loc='best')
    plt.title(r'Focus confinement along x-axis', fontsize=12)
    ax.grid()

    if savefig != '':
        plt.savefig('{}{}_res{}_focus.png'.format(savefig, fname, bsw.sim.resolution), bbox_inches='tight')
    else:
        plt.show()
