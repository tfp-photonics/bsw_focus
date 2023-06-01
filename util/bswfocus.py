#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import traceback
import meep as mp
import numpy as np
from scipy.signal import savgol_filter
from scipy.interpolate import UnivariateSpline
from lmfit.models import GaussianModel
from util.geometry import meep_from_design


class BSWFocus(object):
    def __init__(self, **kwargs):
        self.defaults = {
            'n_hi': 1.3,
            'n_lo': 1.2,
            'wavelength': 1.5555,
            'source_width': 20.0,
            'sim_resolution': 5,
            'sx': 20,
            'sy': 50,
            'cell_pad_x': 0,
            'box_sx': 1,
            'box_sy': 1,
            'design_xr': (-10, 10),
            'design_yr': (0, 20),
            'focus_xr': (-10, 10),
            'focus_yr': (-5, -25),
            'dpml': 2.0,
            'use_complex': True,
            'use_symmetry': True,
            'use_filter': False,
            'k_point': (0, 1, 0),
            'design_matrix': None,
            'spacing': 0.0,
        }
        self.from_kwargs(**kwargs)

        if self.k_point:
            self.k_point = mp.Vector3(*self.k_point)
        self.cell = mp.Vector3(2 * self.cell_pad_x + self.sx + 2 * self.dpml, self.sy + 2 * self.dpml)
        self.current_field = np.nan
        self.last_field = np.nan
        self.field_component = mp.Ex
        self.eps_lo = np.square(self.n_lo)
        self.eps_hi = np.square(self.n_hi)
        self.sources = [mp.Source(mp.ContinuousSource(wavelength=self.wavelength, width=self.source_width),
                                  component=mp.Hz,
                                  center=mp.Vector3(0, self.sy / 2),
                                  size=mp.Vector3(self.cell[0], 0))]
        self.symmetry = [mp.Mirror(direction=mp.X, phase=-1)] if self.use_symmetry else []
        self.pml_layers = [mp.PML(self.dpml)]
        self.design = []
        self.sim = None

    def stop_sim(self, *args):
        """Stops the simulation if field did not change between last time steps"""
        if np.allclose(self.current_field, self.last_field):
            return True
        return False

    def set_design(self, design, xr=None, yr=None):
        """Sets the simulation geometry.
        The design can be either a list of meep geometry objects or a design matrix.
        """
        if type(design) == list:
            self.design = design
        else:
            if xr is None:
                xr = self.design_xr
            if yr is None:
                yr = self.design_yr
            self.design_matrix = design
            self.design = meep_from_design(design, xr, yr, self.eps_hi, self.spacing)


    def append_design(self, design, xr=None, yr=None):
        """Appends meep geometry objects to the simulation geometry.
        The design can be either a list of meep geometry objects or a design matrix.
        """
        if type(design) == list:
            self.design += design
        else:
            if xr is None:
                xr = self.design_xr
            if yr is None:
                yr = self.design_yr
            self.design_matrix = design
            self.design += meep_from_design(design, xr, yr, self.eps_hi, self.spacing)

    def init_sim(self):
        """Initializes the simulation object"""
        self.sim = mp.Simulation(cell_size=self.cell,
                                 geometry=self.design,
                                 sources=self.sources,
                                 boundary_layers=self.pml_layers,
                                 default_material=mp.Medium(epsilon=self.eps_lo),
                                 force_complex_fields=self.use_complex,
                                 symmetries=self.symmetry,
                                 k_point=self.k_point,
                                 resolution=self.sim_resolution)

    def next_field(self, *args):
        """Stores current and last electric field matrix for stop condition"""
        self.last_field = self.current_field
        field = self.sim.get_array(center=mp.Vector3(0, 0, 0),
                                   size=self.sim.cell_size,
                                   component=self.field_component)
        self.current_field = np.linalg.norm(field)

    def get_focus_y(self, xr=None, yr=None, use_filter=None):
        """Returns the y-axis location of highest electric field amplitude"""
        if xr is None:
            xr = self.focus_xr
        if yr is None:
            yr = self.focus_yr
        if use_filter is None:
            use_filter = self.use_filter
        field_y = self.sim.get_array(center=mp.Vector3(np.mean(xr), np.mean(yr)),
                                  size=mp.Vector3(0, np.abs(yr[1] - yr[0])),
                                  component=self.field_component)
        field_y = np.square(np.abs(field_y)).T
        if use_filter:
            savg_field_y = self.get_filter(field_y)
            yloc = np.mean(np.where(savg_field_y == savg_field_y.max())[0][:])
        else:
            yloc = np.mean(np.where(field_y == field_y.max())[0][:])
        return np.abs(yr[1] - yr[0]) / 2 - yloc / self.sim.resolution

    def get_filter(self, data, order=2):
        """Returns filtered data (useful for large oscillations)"""
        return savgol_filter(data, 2 * round(data.shape[0] / 16) - 1, order)

    def get_focus_box_field(self, xr=None, yr=None, box_sx=None, box_sy=None, use_filter=None):
        """Returns the electric field around the spot of highest field amplitude"""
        if xr is None:
            xr = self.focus_xr
        if yr is None:
            yr = self.focus_yr
        if box_sx is None:
            box_sx = self.box_sx
        if box_sy is None:
            box_sy = self.box_sy
        if use_filter is None:
            use_filter = self.use_filter
        y = self.get_focus_y(xr, yr, use_filter)
        box_xy = self.sim.get_array(center=mp.Vector3(np.mean(xr), np.mean(yr) - y),
                                    size=mp.Vector3(box_sx, box_sy),
                                    component=self.field_component)
        return np.abs(box_xy)

    def get_focus_intensity_fit(self, xr=None, yr=None, sx=None, use_filter=None):
        """Returns Gaussian fit to focus spot"""
        if xr is None:
            xr = self.focus_xr
        if yr is None:
            yr = self.focus_yr
        if sx is None:
            sx = self.box_sx
        if use_filter is None:
            use_filter = self.use_filter
        y = self.get_focus_y(xr, yr, use_filter)
        fy = self.sim.get_array(center=mp.Vector3(np.mean(xr), np.mean(yr) - y),
                                size=mp.Vector3(sx, 0),
                                component=self.field_component)
        fy = np.square(np.abs(fy))
        fx = np.linspace(-fy.shape[0] / (2 * self.sim.resolution),
                         fy.shape[0] / (2 * self.sim.resolution), fy.shape[0])
        model = GaussianModel()
        pars = model.guess(fy, x=fx)
        out = model.fit(fy, pars, x=fx)
        return fx, fy, out

    def get_focus_fwhm(self, xr=None, yr=None, sx=None):
        """Gets fwhm by finding roots of spline."""
        if xr is None:
            xr = self.focus_xr
        if yr is None:
            yr = self.focus_yr
        if sx is None:
            sx = self.box_sx
        y = self.get_focus_y(xr, yr, use_filter=False)
        fy= self.sim.get_array(center=mp.Vector3(np.mean(xr), np.mean(yr) - y),
                               size=mp.Vector3(sx, 0),
                               component=self.field_component)
        fy_all = self.sim.get_array(center=mp.Vector3(np.mean(xr), np.mean(yr) - y),
                                    size=mp.Vector3(self.sim.cell_size.x, 0),
                                    component=self.field_component)
        fy_all = np.square(np.abs(fy_all))
        fy_all -= np.min(fy_all)
        fx_all = np.linspace(-fy_all.shape[0] / (2 * self.sim.resolution),
                             fy_all.shape[0] / (2 * self.sim.resolution),
                             fy_all.shape[0])
        fy = np.square(np.abs(fy))
        fy -= np.min(fy)
        allmin = np.where(fy == np.min(fy))[0]
        midmin = float(len(allmin)) / 2.
        min1, min2 = allmin[int(midmin - 0.5)], allmin[int(midmin + 0.5)]
        fy_foc = fy[min1:min2+1]
        fx_foc = np.linspace(-fy_foc.shape[0] / (2 * self.sim.resolution),
                             fy_foc.shape[0] / (2 * self.sim.resolution), fy_foc.shape[0])
        if fy_foc.any() and fx_foc.any():
            spline = UnivariateSpline(fx_foc, fy_foc - np.max(fy_foc) / 2., s=0)
        else:
            spline = None
        return fx_all, fy_all, fx_foc, fy_foc, spline, np.mean(yr) - y

    def run(self):
        """Runs the simulation"""
        self.init_sim()
        self.stop = False
        self.last_field = np.nan
        self.current_field = np.nan
        self.sim.run(mp.at_every(10, self.next_field),
                     until=self.stop_sim)

    def from_kwargs(self, **kwargs):
        """Restore class settings from dict"""
        sk, sd = set(kwargs), set(self.defaults)
        try:
            for k in sk - sd:
                raise KeyError
        except KeyError as c:
            traceback.print_exc(file=sys.stdout)
            print('Class {}() has no attribute {}'.format(self.__class__.__name__, k))
            sys.exit(1)
        for k in sd - sk:
            setattr(self, k, self.defaults[k])
        for k in sk & sd:
            #FIXME this does not load variables that may change types
            v = kwargs.get(k)
            if v is None:
                setattr(self, k, v)
            elif np.isnan(v).any():
                setattr(self, k, None)
            else:
                setattr(self, k, type(self.defaults[k])(v))

    def to_dict(self):
        """Return relevant simulation information from class dict.
        Converts NoneType to np.nan for hdf5 compatibility.
        """
        return {k: (np.nan if vars(self)[k] is None else vars(self)[k]) for k in self.defaults.keys()}

