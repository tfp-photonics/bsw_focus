#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# filter annoying and benign warnings
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
warnings.simplefilter(action='ignore', category=FutureWarning)

import os
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
        self.infile = config.infile
        self.outputdir = config.outputdir
        self.outfile = self.outputdir + os.path.splitext(os.path.basename(self.infile))[0] + '_toggle.h5'

        self.logger.info("Using file {}.".format(self.infile))

        h5f = h5py.File(config.infile, 'r')
        d = {k: h5f['sim'][k].value for k in h5f['sim'].keys()}
        self.field_list = list(h5f['focus'])
        self.max_field = self.field_list[-1]
        self.M_list = list(h5f['design'])
        self.Ml = self.M_list[-1][:int(self.M_list[-1].shape[0] / 2)]
        h5f.close()

        # d.update({
        #     'sim_resolution': config.res,
        # })

        self.dim = self.Ml.shape[1]
        self.res = d['sim_resolution']
        self.design_yr = d['design_yr']
        self.focus_yr = d['focus_yr']
        self.box_sx = d['box_sx']
        self.box_sy = d['box_sy']
        self.space = d['spacing']
        self.n_lo = d['n_lo']
        self.n_hi = d['n_hi']

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

        field_list = self.field_list
        max_field = self.max_field
        t = []
        M_list = self.M_list
        Ml = self.Ml

        self.logger.debug("Initial matrix:\n{}".format(Ml))

        # optimization control
        margin = 2
        margin_counter = 0
        toggle_counter = np.zeros_like(Ml)
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
            for i1, i2 in np.transpose(np.where(Ml == 1)):
                tMl = np.copy(Ml)
                tMl[i1, i2] = 0
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

            if margin_counter <= margin and toggle_counter[int(idx[0]), int(idx[1])] <= margin + 2:
                val = Ml[int(idx[0]), int(idx[1])]
                if val == 0:
                    Ml[int(idx[0]), int(idx[1])] = 1
                else:
                    Ml[int(idx[0]), int(idx[1])] = 0
                toggle_counter[int(idx[0]), int(idx[1])] += 1
            else:
                Ml = Ml_bak
                break

            self.logger.debug("Matrix after iteration {}:\n{}".format(iterations, Ml))

            for rank in waitlist:
                self.logger.debug("Send CONTINUE to slave {}.".format(rank))
                self.comm.send(None, dest=rank, tag=Tags.CONTINUE)

            if iterations % 10 == 0:
                self.create_output(self.outfile, np.array(M_list), np.array(field_list), np.array(t))

        # let slaves exit gracefully
        for rank in range(1, self.size):
            self.logger.debug("Send STOP to slave {}.".format(rank))
            self.comm.send(None, dest=rank, tag=Tags.STOP)
            self.comm.recv(None, source=rank, tag=Tags.STOP)

        self.logger.info("Optimization finished in {} iterations.".format(iterations))
        self.create_output(self.outfile, np.array(M_list), np.array(field_list), np.array(t))

    def slave(self):
        mystatus = Tags.READY
        while True:
            self.logger.debug("Send STATUS: {}.".format(mystatus))
            self.comm.send(None, dest=0, tag=mystatus)
            data = self.comm.recv(source=0, status=self.status)
            tag = self.status.Get_tag()
            if tag == Tags.START:
                self.logger.debug("Received START.")
                i, j, tM = data
                field = self.get_sim_field(self.create_sim(tM))
                self.logger.debug("Field: {}.".format(field))
                self.logger.debug("Send DONE.")
                self.comm.send((i, j, field), dest=0, tag=Tags.DONE)
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
                       focus_yr=self.focus_yr,
                       n_lo=self.n_lo,
                       n_hi=self.n_hi,
                       spacing=self.space,
                       box_sx=self.box_sx,
                       box_sy=self.box_sy)
        bsw.set_design(matrix)
        return bsw

    def get_sim_field(self, bsw):
        bsw.run()
        field = bsw.get_focus_box_field()
        return np.square(np.linalg.norm(field))

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
    p = configargparse.ArgParser(default_config_files=['./resources/config_toggle.ini'])
    p.add('-c', '--config', is_config_file=True, help="Custom config file path")
    p.add('--outputdir', type=str, help="Directory for optimization results")
    p.add('--logconf', type=str, help="Logging config file")
    p.add('--res', type=int, help="Resolution for simulations")
    p.add('--infile', type=str, help="Input optimization file", required=True)
    options = p.parse_args()

    opt = BSWOpt(options)
    try:
        opt.start()
    except KeyboardInterrupt:
        opt.stop()
