#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import meep as mp
import numpy as np


def make_geometry(design, xr, yr, width=None, height=None, spacing=0.0):
    if not design.any():
        return []

    nx, ny = design.shape[0], design.shape[1]
    sx, sy = np.abs(xr[1] - xr[0]), np.abs(yr[1] - yr[0])
    cx, cy = np.mean(xr), np.mean(yr)

    if width is None:
        width = np.round(sx / nx, 2) - spacing

    if height is None:
        height = np.round(sy / ny, 2) - spacing

    px, py = width + spacing, height + spacing

    x_range = np.linspace(cx - px * (nx - 1) / 2, cx + px * (nx - 1) / 2, nx)
    y_range = np.linspace(cy - py * (ny - 1) / 2, cy + py * (ny - 1) / 2, ny)
    out = []
    for i, j in np.transpose(np.where(design == 1)):
        out.append([x_range[i], y_range[j], width, height])
    return np.asarray(out)


def meep_from_design_rotate(design, xr, yr, eps, angle):
    geom = make_geometry(design, xr, yr)
    out = []
    rad = np.deg2rad(angle)
    e1 = mp.Vector3(1, 0, 0).rotate(mp.Vector3(0, 0, 1), rad)
    e2 = mp.Vector3(0, 1, 0).rotate(mp.Vector3(0, 0, 1), rad)
    for cx, cy, w, h in geom:
        cxr, cyr, _ = mp.Vector3(cx, cy - 21).rotate(mp.Vector3(0, 0, 1), rad)
        cyr += 15
        out.append(mp.Block(size=mp.Vector3(w, h, 0),
                            center=mp.Vector3(cxr, cyr, 0),
                            e1=e1, e2=e2,
                            material=mp.Medium(epsilon=eps)))
    return out


def meep_from_design(design, xr, yr, eps, spacing):
    geom = make_geometry(design, xr, yr, spacing=spacing)
    out = []
    for cx, cy, w, h in geom:
        out.append(mp.Block(size=mp.Vector3(w, h, 0),
                            center=mp.Vector3(cx, cy, 0),
                            material=mp.Medium(epsilon=eps)))
    return out


def make_isosceles(xr, yr, n):
    eps = np.square(n)
    tri = [meep.Cone(radius=np.abs(xr[1] - xr[0]) / 2,
                     height=np.abs(yr[1] - yr[0]),
                     center=meep.Vector3(np.mean(xr), np.mean(yr)),
                     material=meep.Medium(epsilon=eps),
                     axis=meep.Vector3(0, -1, 0))]
    return tri
