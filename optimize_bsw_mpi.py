#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# filter annoying and benign warnings
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
warnings.simplefilter(action='ignore', category=FutureWarning)

import time
import signal
import logging
import logging.config
import configargparse
from datetime import datetime
import h5py
import numpy as np
from mpi4py import MPI

# own modules
from util.bswfocus import BSWFocus


# MPI tags (basically an enum)
class Tags(object):
    READY = 0
    DONE = 1
    STOP = 2
    START = 3
    WAIT = 4
    CONTINUE = 5


class BSWOpt(object):
    def __init__(self, config):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        self.status = MPI.Status()
        logging.config.fileConfig(config.logconf)
        self.logger = logging.getLogger("Rank {:0{width}d}".format(self.rank, width=len(str(self.size))))
        self.dim_x = config.dimx
        self.dim_y = config.dimy
        self.res = config.res
        self.design_yr = config.design_yr
        self.design_xr = config.design_xr
        self.sx = config.sx
        self.focus_yr = config.focus_yr
        self.box_sx = config.boxx
        self.box_sy = config.boxy
        self.space = config.space
        self.n_lo = config.nlo
        self.n_hi = config.nhi
        self.outputdir = config.outputdir
        self.tstamp = datetime.strftime(datetime.now(), '%Y%m%d-%H%M%S')
        self.infile = config.infile
        self.loss = config.loss

    def start(self):
        if self.size < 2:
            self.logger.error("MPI size must be greater than 1!")
        elif self.rank == 0:
            self.master()
        else:
            self.slave()
        self.stop()

    def stop(self):
        time.sleep(0.5)
        MPI.Finalize()
        time.sleep(0.5)

    def master(self):
        self.logger.info("Using {} processes.".format(self.size))

        if self.infile is None:
            fname = '{}{}_bsw_{}x{}_res{}.h5'.format(self.outputdir, self.tstamp, self.dim_x, self.dim_y, self.res)
            self.logger.info("No input file specified, creating {}.".format(fname))
            field_list = [0]
            max_field = 0
            M_list = []
            Ml = np.zeros((int(self.dim_x / 2), self.dim_y))
            t = []
        else:
            fname = infile
            self.logger.info("Using existing optimization {}.".format(fname))
            h5f = h5py.File(fname, 'r')
            field_list = list(h5f['focus'])
            max_field = field_list[-1]
            t = list(h5f['it_time'])
            M_list = list(h5f['design'])
            Ml = M_list[-1][:int(M_list[-1].shape[0] / 2)]
            h5f.close()

        self.logger.debug("Initial matrix:\n{}".format(Ml))

        # optimization control
        margin = 2
        margin_counter = 0
        Ml_bak = None
        first_neg = True
        iterations = 0

        while True:
            tasks = []
            for i1, i2 in np.transpose(np.where(Ml == 0)):
                tMl = np.copy(Ml)
                tMl[i1, i2] = 1
                tM = np.vstack((tMl, np.flipud(tMl)))
                tasks.append((i1, i2, tM))
            res_fields = []
            res_idx = []
            waitlist = []
            total_tasks = len(tasks)
            distributed_tasks = 0
            t.append(time.time())

            while True:
                self.logger.debug("Receiving...")
                self.status = MPI.Status()
                data = self.comm.recv(source=MPI.ANY_SOURCE, tag=MPI.ANY_TAG, status=self.status)
                source = self.status.Get_source()
                tag = self.status.Get_tag()

                if tag == Tags.DONE:
                    self.logger.debug("Received DONE from slave {}.".format(source))
                    res_idx.append((data[0], data[1]))
                    res_fields.append(data[2])
                elif tag == Tags.READY:
                    self.logger.debug("Received READY from slave {}.".format(source))
                    if not tasks or distributed_tasks == total_tasks:
                        self.logger.debug("Send WAIT to slave {}.".format(source))
                        self.comm.send(None, dest=source, tag=Tags.WAIT)
                        waitlist.append(source)
                    else:
                        self.logger.debug("Send START to slave {}.".format(source))
                        self.comm.send(tasks.pop(), dest=source, tag=Tags.START)
                        distributed_tasks += 1
                if tag == Tags.WAIT:
                    self.logger.debug("Received WAIT from slave {}.".format(source))
                    if len(waitlist) == self.size - 1:
                        break

            res_idx = np.array(res_idx)
            res_fields = np.array(res_fields)
            if not res_idx.any() or not res_fields.any():
                if margin_counter > 0:
                    Ml = Ml_bak
                break

            field = res_fields[np.argmax(res_fields)]
            idx = res_idx[np.argmax(res_fields)]

            iterations += 1
            self.logger.info("Iteration {:<6d}, dE = {}".format(iterations, field - max_field))

            if field < max_field:
                margin_counter += 1
                if first_neg:
                    Ml_bak = np.copy(Ml)
                    first_neg = False
            else:
                max_field = field
                field_list.append(max_field)
                M_list.append(np.vstack((Ml, np.flipud(Ml))))
                margin_counter = 0
                first_neg = True

            if margin_counter <= margin:
                Ml[int(idx[0]), int(idx[1])] = 1
            else:
                Ml = Ml_bak
                break

            self.logger.debug("Matrix after iteration {}:\n{}".format(iterations, Ml))

            for rank in waitlist:
                self.logger.debug("Send CONTINUE to slave {}.".format(rank))
                self.comm.send(None, dest=rank, tag=Tags.CONTINUE)

            if iterations % 10 == 0:
                self.create_output(fname, np.array(M_list), np.array(field_list), np.array(t))

        # let slaves exit gracefully
        for rank in range(1, self.size):
            self.logger.debug("Send STOP to slave {}.".format(rank))
            self.comm.send(None, dest=rank, tag=Tags.STOP)
            self.comm.recv(None, source=rank, tag=Tags.STOP)

        self.logger.info("Optimization finished in {} iterations.".format(iterations))
        self.create_output(fname, np.array(M_list), np.array(field_list), np.array(t))

    def slave(self):
        mystatus = Tags.READY
        while True:
            self.logger.debug("Send STATUS: {}.".format(mystatus))
            self.comm.send(None, dest=0, tag=mystatus)
            self.status = MPI.Status()
            data = self.comm.recv(source=0, tag=MPI.ANY_TAG, status=self.status)
            tag = self.status.Get_tag()
            if tag == Tags.START:
                self.logger.debug("Received START.")
                i, j, tM = data
                bsw = self.create_sim(tM)
                bsw.run()
                loss = self.get_loss(bsw)
                self.logger.debug("Loss: {}.".format(loss))
                self.logger.debug("Send DONE.")
                self.comm.send((i, j, loss), dest=0, tag=Tags.DONE)
                mystatus = Tags.READY
            elif tag == Tags.WAIT:
                self.logger.debug("Received WAIT.")
                mystatus = Tags.WAIT
            elif tag == Tags.CONTINUE:
                self.logger.debug("Received CONTINUE.")
                mystatus = Tags.READY
            elif tag == Tags.STOP:
                self.logger.debug("Received STOP.")
                mystatus = Tags.STOP
                break
        # cleanup
        self.comm.send(None, dest=0, tag=mystatus)

    def create_sim(self, matrix=[]):
        bsw = BSWFocus(sim_resolution=self.res,
                       design_yr=self.design_yr,
                       design_xr=self.design_xr,
                       sx=self.sx,
                       focus_yr=self.focus_yr,
                       n_lo=self.n_lo,
                       n_hi=self.n_hi,
                       spacing=self.space,
                       box_sx=self.box_sx,
                       box_sy=self.box_sy)
        bsw.set_design(matrix)
        return bsw

    def get_loss(self, bsw):
        if self.loss == 'field':
            # max field loss. simple, effective.
            field = bsw.get_focus_box_field()
            out = np.square(np.linalg.norm(field))
        elif self.loss == 'fwhm':
            # pure fwhm loss
            _, _, spline = bsw.get_focus_fwhm(sx=3)
            if spline is not None:
                roots = spline.roots()
                middle = float(len(roots)) / 2.
                r1, r2 = roots[int(middle - 0.5)], roots[int(middle + 0.5)]
                fwhm = np.abs(r2 - r1)
                out = 1. / np.square(fwhm)
            else:
                out = 0
        elif self.loss == 'combined':
            # require a certain field strength, then optimize for fwhm
            field = np.linalg.norm(bsw.get_focus_box_field())
            _, _, spline = bsw.get_focus_fwhm(sx=3)
            if spline is not None and field > 1:
                roots = spline.roots()
                middle = float(len(roots)) / 2.
                r1, r2 = roots[int(middle - 0.5)], roots[int(middle + 0.5)]
                ifwhm = 1. / np.abs(r2 - r1)
                out = np.square(field) + np.square(ifwhm)
            else:
                out = np.square(field)
        return out

    def create_output(self, fname, m, e, t):
        h5f = h5py.File(fname, 'w')
        h5f.create_dataset('design', data=m)
        h5f.create_dataset('focus', data=e)
        h5f.create_dataset('it_time', data=t)
        bsw = self.create_sim()
        simgrp = h5f.create_group('sim')
        for key, value in bsw.to_dict().items():
            simgrp.create_dataset(key, data=value)
        h5f.close()


if __name__ == '__main__':
    p = configargparse.ArgParser(default_config_files=['./resources/config.ini'])
    p.add('-c', '--config', is_config_file=True, help="Custom config file path")
    p.add('--outputdir', type=str, help="Directory for optimization results")
    p.add('--logconf', type=str, help="Logging config file")
    p.add('--dimx', type=int, help="Dimensions of optimization matrix along x-axis, needs to be an even number")
    p.add('--dimy', type=int, help="Dimensions of optimization matrix along y-axis")
    p.add('--res', type=int, help="Resolution for simulations")
    p.add('--nlo', type=float, help="Refractive index of material 1 (low)")
    p.add('--nhi', type=float, help="Refractive index of material 2 (high)")
    p.add('--space', type=float, help="Space to leave between pixels (may be negative)")
    p.add('--boxx', type=float, help="Width of optimization focus box")
    p.add('--boxy', type=float, help="Height of optimization focus box")
    p.add('--design_yr', type=float, nargs=2, help="Design space y-range")
    p.add('--design_xr', type=float, nargs=2, help="Design space x-range")
    p.add('--sx', type=float, help="Cell size in x")
    p.add('--sy', type=float, help="Cell size in y")
    p.add('--focus_yr', type=float, nargs=2, help="Optimization target y-range")
    p.add('--infile', type=str, help="Input optimization file")
    p.add('--loss', type=str, help="Method of calculating loss function")
    options = p.parse_args()

    opt = BSWOpt(options)
    try:
        opt.start()
    except KeyboardInterrupt:
        opt.stop()
