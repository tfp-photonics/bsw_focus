#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt


def main():
    feature_size = []
    fwhm = []
    data = []
    with open('./fwhm/info.txt', 'r') as f:
        f.readline()
        for line in f:
            elements = line.split()
            feature_size.append(float(elements[3]))
            data.append([
                float(elements[3]),
                float(elements[4]),
                float(elements[5]),
            ])

    data = np.array(data)
    data = data[data[:, 0].argsort()[::-1]]

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{siunitx} \usepackage{physics}')
    plt.plot(data[:, 0], data[:, 1], 'k--', lw=0.7)
    plt.scatter(data[:, 0], data[:, 1], c='r', marker='x')
    plt.xlim([max(data[:, 0]), min(data[:, 0])])
    plt.title(r'Feature size \& FWHM', fontsize=12)
    plt.xlabel(r'Feature size (\SI{}{\micro\meter})', fontsize=10)
    plt.ylabel(r'FWHM', fontsize=10)
    plt.grid()
    plt.tight_layout()
    plt.savefig('fwhm/feat_fwhm.png', dpi=300, bbox_inches='tight')
    plt.close()

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.rc('text.latex', preamble=r'\usepackage{amsmath} \usepackage{siunitx} \usepackage{physics}')
    plt.plot(data[:, 0], data[:, 2], 'k--', lw=0.7)
    plt.scatter(data[:, 0], data[:, 2], c='r', marker='x')
    plt.xlim([max(data[:, 0]), min(data[:, 0])])
    plt.title(r'Feature size \& focus distance', fontsize=12)
    plt.xlabel(r'Feature size (\SI{}{\micro\meter})', fontsize=10)
    plt.ylabel(r'Focus distance (\SI{}{\micro\meter})', fontsize=10)
    plt.grid()
    plt.tight_layout()
    plt.savefig('fwhm/feat_dist.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    main()
