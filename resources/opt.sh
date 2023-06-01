#!/bin/bash

MPIARGS="--bind-to-core --bycore --hostfile resources/hosts -x PATH"
PYTHON="/scratch/local/.virtualenvwrapper/meep/bin/python3"

# mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 20 --dimy 5 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 9.3 8.3 --sx 40
# mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 24 --dimy 6 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 9.3 8.3 --sx 40
# mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 28 --dimy 7 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 9.3 8.3 --sx 40
# mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 32 --dimy 8 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 9.3 8.3 --sx 40
# mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 36 --dimy 9 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 9.3 8.3 --sx 40
# mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 44 --dimy 11 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 9.3 8.3 --sx 40
# mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 48 --dimy 12 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 9.3 8.3 --sx 40
# mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 52 --dimy 13 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 9.3 8.3 --sx 40
# mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 56 --dimy 14 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 9.3 8.3 --sx 40
# mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 68 --dimy 17 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 9.3 8.3 --sx 40
# mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 80 --dimy 20 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 9.3 8.3 --sx 40

mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 20 --dimy 5 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40
mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 24 --dimy 6 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40
mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 28 --dimy 7 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40
mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 32 --dimy 8 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40
mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 36 --dimy 9 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40
mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 40 --dimy 10 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40
mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 44 --dimy 11 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40
mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 48 --dimy 12 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40
mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 52 --dimy 13 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40
mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 56 --dimy 14 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40
mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 60 --dimy 15 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40
mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 68 --dimy 17 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40
mpiexec $MPIARGS $PYTHON optimize_bsw_mpi.py --dimx 80 --dimy 20 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 12.5 --sx 40

mv /users/tfp/yaugenst/code/src/tfp/tfp-code/bsw-focus/output/base/* /scratch/local/paper_data/1um/sim/
mv /users/tfp/yaugenst/code/src/tfp/tfp-code/bsw-focus/*.log /scratch/local/paper_data/1um/sim/

$PYTHON /users/tfp/yaugenst/code/src/tfp/tfp-code/bsw-focus/overlay_and_fwhm_plots.py -f /scratch/local/paper_data/1um/sim/*.h5 -r 20 -s /scratch/local/paper_data/1um/info_plots/
mv /users/tfp/yaugenst/code/src/tfp/tfp-code/bsw-focus/info.txt /scratch/local/paper_data/1um/info_plots/

$PYTHON /users/tfp/yaugenst/code/src/tfp/tfp-code/bsw-focus/output_hdf5.py -f /scratch/local/paper_data/1um/sim/*.h5
