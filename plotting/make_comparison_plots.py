#!/usr/bin/env python3

import h5py
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import scipy.interpolate as inter

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
    ['20180327-021417_bsw_10x10', 'm2'],
    ['20180402-230449_bsw_6x12', 'q8'],
]

name = names[8]

h5f = h5py.File('/scratch/local/data/fields/{}_res5_fields.h5'.format(name[0]), 'r')
sim_ex = np.asarray(h5f['Ex']).T
sim_ey = np.asarray(h5f['Ey']).T
sim_eps = np.asarray(h5f['Dielectric']).T
h5f.close()

intensity_sim = np.absolute(sim_ex)[150:950]
intensity_sim /= intensity_sim.max()
phase_sim = -np.angle(sim_ex, deg=True)[150:950]
mx_sim = np.round(np.mean(np.where(intensity_sim >= np.max(intensity_sim) - np.max(intensity_sim) / 3.), axis=1))

intensity_sim_close = intensity_sim[int(mx_sim[0] - 150):int(mx_sim[0] + 150),
                                    int(mx_sim[1] - 150):int(mx_sim[1] + 150)]
intensity_sim_close /= intensity_sim_close.max()
phase_sim_close = phase_sim[int(mx_sim[0] - 150):int(mx_sim[0] + 150),
                            int(mx_sim[1] - 150):int(mx_sim[1] + 150)]

h5f = h5py.File('/scratch/local/data/snom/{}_snom.h5'.format(name[1]), 'r')
intensity = np.asarray(h5f['intensity'])
intensity_close = np.asarray(h5f['intensity_close'])
phase = np.asarray(h5f['phase'])
phase_close = np.asarray(h5f['phase_close'])
h5f.close()


# rescale the data so we have arrays of the same size

vals = np.reshape(intensity, (intensity.shape[0] * intensity.shape[1]))
pts = np.asarray([[i, j] for i in np.linspace(0, 1, intensity.shape[0]) for j in np.linspace(0, 1, intensity.shape[1])])
grid_x, grid_y = np.mgrid[0:1:intensity_sim.shape[0] * 1j,
                          0:1:intensity_sim.shape[1] * 1j]
intensity = inter.griddata(pts, vals, (grid_x, grid_y), method='linear')
intensity /= intensity.max()

vals = np.reshape(phase, (phase.shape[0] * phase.shape[1]))
pts = np.asarray([[i, j] for i in np.linspace(0, 1, phase.shape[0]) for j in np.linspace(0, 1, phase.shape[1])])
grid_x, grid_y = np.mgrid[0:1:phase_sim.shape[0] * 1j,
                          0:1:phase_sim.shape[1] * 1j]
phase = inter.griddata(pts, vals, (grid_x, grid_y), method='cubic')

mx = np.round(np.mean(np.where(intensity >= np.max(intensity) - np.max(intensity) / 4.), axis=1))
mx_close = np.round(np.mean(np.where(intensity_close >= np.max(intensity_close) - np.max(intensity_close) / 4.), axis=1))
intensity_close = intensity_close[int(mx_close[0] - 50):int(mx_close[0] + 50),
                                  int(mx_close[1] - 50):int(mx_close[1] + 50)]
phase_close = phase_close[int(mx_close[0] - 50):int(mx_close[0] + 50),
                          int(mx_close[1] - 50):int(mx_close[1] + 50)]

vals = np.reshape(intensity_close, (intensity_close.shape[0] * intensity_close.shape[1]))
pts = np.asarray([[i, j] for i in np.linspace(0, 1, intensity_close.shape[0]) for j in np.linspace(0, 1, intensity_close.shape[1])])
grid_x, grid_y = np.mgrid[0:1:intensity_sim_close.shape[0] * 1j,
                          0:1:intensity_sim_close.shape[1] * 1j]
intensity_close = inter.griddata(pts, vals, (grid_x, grid_y), method='linear')

vals = np.reshape(phase_close, (phase_close.shape[0] * phase_close.shape[1]))
pts = np.asarray([[i, j] for i in np.linspace(0, 1, phase_close.shape[0]) for j in np.linspace(0, 1, phase_close.shape[1])])
grid_x, grid_y = np.mgrid[0:1:phase_sim_close.shape[0] * 1j,
                          0:1:phase_sim_close.shape[1] * 1j]
phase_close = inter.griddata(pts, vals, (grid_x, grid_y), method='cubic')


# plots

plt.rc('text', usetex=True)
plt.rc('font', family='serif')
plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{siunitx} \usepackage{physics}')


fig, ax = plt.subplots(1, 2, dpi=300, sharey=True)
xticks = np.linspace(0, intensity[150:250].shape[0], 5)
xticklabels = np.linspace(0, intensity[150:250].shape[0] / 20, 5, dtype=int)
ax[0].set_title(r'Focus amplitude along x-axis')
ax[0].plot(intensity_sim[int(mx_sim[0]), 150:250], c='k', label=r'Simulation')
ax[0].plot(intensity[int(mx[0]), 150:250], c='r', label=r'SNOM')
ax[0].set_xticks(xticks)
ax[0].set_xticklabels(xticklabels)
ax[0].set_xlabel(r'x (\SI{}{\micro\meter})', fontsize=10)
ax[0].set_ylabel(r'amplitude', fontsize=10)
plt.tight_layout()

xticks = np.linspace(0, intensity.shape[0], 5)
xticklabels = np.linspace(0, intensity.shape[0] / 20, 5, dtype=int)
ax[1].set_title(r'Focus amplitude along z-axis')
ax[1].plot(intensity_sim[:, int(mx_sim[1])], c='k', label=r'Simulation')
ax[1].plot(intensity[:, int(mx[1])], c='r', label=r'SNOM')
ax[1].set_xticks(xticks)
ax[1].set_xticklabels(xticklabels)
ax[1].set_xlabel(r'x (\SI{}{\micro\meter})', fontsize=10)
ax[1].legend(loc=(1.1, 0.9))
plt.tight_layout()
plt.savefig('focus_comparison_{}.png'.format(name[1]), dpi=300)


fig, ax = plt.subplots(2, 4, dpi=400)

ax[0][0].imshow(intensity, cmap='hot')
ax[0][0].set_title(r'snom\_all')
ax[0][1].imshow(intensity_close, cmap='hot')
ax[0][1].set_title(r'snom\_close')
ax[0][2].imshow(phase, cmap='hot')
ax[0][2].set_title(r'snom\_phase')
ax[0][3].imshow(phase_close, cmap='hot')
ax[0][3].set_title(r'snom\_phase\_close')
ax[1][0].imshow(intensity_sim, cmap='hot')
ax[1][0].set_title(r'sim\_all')
ax[1][1].imshow(intensity_sim_close, cmap='hot')
ax[1][1].set_title(r'sim\_close')
ax[1][2].imshow(phase_sim, cmap='hot')
ax[1][2].set_title(r'sim\_phase')
ax[1][3].imshow(phase_sim_close, cmap='hot')
ax[1][3].set_title(r'sim\_phase\_close')

for i in range(2):
    ax[i][0].set_ylabel(r'z (\SI{}{\micro\meter})', fontsize=10)
    for j in range(4):
        if j % 2 == 0:
            xticks = np.linspace(0, intensity.shape[0], 5)
            xticklabels = np.linspace(0, intensity.shape[0] / 20, 5, dtype=int)
            yticks = np.linspace(0, intensity.shape[1], 4)
            yticklabels = np.linspace(intensity.shape[1] / 20, 0, 4, dtype=int)
        else:
            xticks = np.linspace(0, intensity_close.shape[0], 5)
            xticklabels = np.linspace(0, intensity_close.shape[0] / 20, 5, dtype=int)
            yticks = np.linspace(0, intensity_close.shape[1], 4)
            yticklabels = np.linspace(intensity_close.shape[1] / 20, 0, 4, dtype=int)
        ax[i][j].set_xticks(xticks)
        ax[i][j].set_yticks(yticks)
        ax[i][j].set_xticklabels(xticklabels)
        ax[i][j].set_yticklabels(yticklabels)
        ax[i][j].set_xlabel(r'x (\SI{}{\micro\meter})', fontsize=10)

plt.suptitle(r'SNOM \& simulation comparison: {}'.format(name[0].replace('_', '\_')))

plt.tight_layout()
plt.savefig('fields_comparison_{}.png'.format(name[1]), dpi=400)
