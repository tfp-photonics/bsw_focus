#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import argparse
from os.path import basename
from datetime import datetime

import numpy as np

def main():
    with open('./20180413-154357_ids.txt', 'r') as f:
        content = f.readlines()
    content = np.asarray([line.strip('\n').split(' ') for line in content])
    data = []
    for n, cx, cy, l, dn, ibox, fwhm, ifwhm, fn in content:
        data.append([
            str(n), int(cx), int(cy), int(l), float(dn),
            float(ibox), float(fwhm), float(ifwhm), str(fn)
        ])
    data = np.array(data)
    all_data = np.array(data)
    data = data[np.where(data[:, 4] == '0.1')]         # exclude non 0.1 index contrast
    data = data[np.where(data[:, 3] == '1')]           # only layer 1
    _, idx = np.unique(data[:, 8], return_index=True)  # only unique runs
    data = data[idx]
    by_intb = data[np.array(data[:, 5], dtype=np.float).argsort()][::-1][:5]
    by_fwhm = data[np.array(data[:, 6], dtype=np.float).argsort()][:5]
    by_inty = data[np.array(data[:, 7], dtype=np.float).argsort()][::-1][:5]

    top_set = list(set(np.array([by_intb[:, 8], by_fwhm[:, 8], by_inty[:, 8]]).flatten()))
    top_data = all_data[np.isin(all_data[:, 8], top_set)]
    top_data = top_data[np.array(top_data[:, 3], dtype=np.int).argsort()]
    with open('20180413-154357_bestruns_ids.txt', 'w') as f:
        for line in top_data[np.array(top_data[:, 6], dtype=np.float).argsort()]:
            print(' '.join(str(cell) for cell in line), file=f)
    with open('20180413-154357_bestruns.txt', 'w') as f:
        for line in top_set:
            print(line, file=f)


if __name__ == '__main__':
    main()
