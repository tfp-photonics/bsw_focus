#!/bin/bash

MPIARGS="--bind-to-core --bycore --hostfile hosts -x PATH"

# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 10 --res 5 --nlo 1.1 --nhi 1.2
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 20 --res 5 --nlo 1.1 --nhi 1.2
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 30 --res 5 --nlo 1.1 --nhi 1.2
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 40 --res 5 --nlo 1.1 --nhi 1.2

# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 10 --res 5 --nlo 1.1 --nhi 1.2 --space 0.1
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 20 --res 5 --nlo 1.1 --nhi 1.2 --space 0.1
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 30 --res 5 --nlo 1.1 --nhi 1.2 --space 0.1
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 40 --res 5 --nlo 1.1 --nhi 1.2 --space 0.1

# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 10 --res 5 --nlo 1.09 --nhi 1.21
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 20 --res 5 --nlo 1.09 --nhi 1.21
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 30 --res 5 --nlo 1.09 --nhi 1.21
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 40 --res 5 --nlo 1.09 --nhi 1.21

# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 10 --res 5 --nlo 1.1 --nhi 1.2 --focus_yr -15 -20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 20 --res 5 --nlo 1.1 --nhi 1.2 --focus_yr -15 -20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 30 --res 5 --nlo 1.1 --nhi 1.2 --focus_yr -15 -20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 40 --res 5 --nlo 1.1 --nhi 1.2 --focus_yr -15 -20

# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 10 --res 5 --nlo 1.11 --nhi 1.19
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 20 --res 5 --nlo 1.11 --nhi 1.19
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 30 --res 5 --nlo 1.11 --nhi 1.19
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 40 --res 5 --nlo 1.11 --nhi 1.19

# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 10 --res 8 --nlo 1.1 --nhi 1.2
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 20 --res 8 --nlo 1.1 --nhi 1.2
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 30 --res 8 --nlo 1.1 --nhi 1.2
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 40 --res 8 --nlo 1.1 --nhi 1.2

# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 10 --res 7 --nlo 1.1 --nhi 1.2
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 20 --res 7 --nlo 1.1 --nhi 1.2
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 30 --res 7 --nlo 1.1 --nhi 1.2
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 40 --res 7 --nlo 1.1 --nhi 1.2

# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 10 --res 5 --nlo 1.1 --nhi 1.2 --space -0.1
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 20 --res 5 --nlo 1.1 --nhi 1.2 --space -0.1
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 30 --res 5 --nlo 1.1 --nhi 1.2 --space -0.1
# mpiexec $MPIARGS optimize_bsw_mpi.py --dim 40 --res 5 --nlo 1.1 --nhi 1.2 --space -0.1

# toggle with togglemargin = 2
# for f in ./output/done/*.h5; do
#     mpiexec $MPIARGS optimize_toggle.py --infile $f;
# done

# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 6 --dimy 12 --res 5 --design_xr -5 5 --design_yr 4 24 --focus_yr 3.5 -24 --sx 20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 10 --dimy 20 --res 5 --design_xr -5 5 --design_yr 4 24 --focus_yr 3.5 -24 --sx 20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 16 --dimy 32 --res 5 --design_xr -5 5 --design_yr 4 24 --focus_yr 3.5 -24 --sx 20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 20 --dimy 40 --res 5 --design_xr -5 5 --design_yr 4 24 --focus_yr 3.5 -24 --sx 20

# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 10 --dimy 5 --res 5 --design_xr -10 10 --design_yr 14 24 --focus_yr 13.5 -24 --sx 20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 20 --dimy 10 --res 5 --design_xr -10 10 --design_yr 14 24 --focus_yr 13.5 -24 --sx 20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 30 --dimy 15 --res 5 --design_xr -10 10 --design_yr 14 24 --focus_yr 13.5 -24 --sx 20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 40 --dimy 20 --res 5 --design_xr -10 10 --design_yr 14 24 --focus_yr 13.5 -24 --sx 20

# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 20 --dimy 5 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 -24 --sx 40
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 40 --dimy 10 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 -24 --sx 40
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 60 --dimy 15 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 -24 --sx 40

# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 20 --dimy 10 --res 5 --design_xr -20 20 --design_yr 4 24 --focus_yr 3.5 -24 --sx 40
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 40 --dimy 20 --res 5 --design_xr -20 20 --design_yr 4 24 --focus_yr 3.5 -24 --sx 40
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 60 --dimy 30 --res 5 --design_xr -20 20 --design_yr 4 24 --focus_yr 3.5 -24 --sx 40

# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 6 --dimy 12 --res 5 --design_xr -5 5 --design_yr 4 24 --focus_yr 0 -24 --sx 20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 10 --dimy 20 --res 5 --design_xr -5 5 --design_yr 4 24 --focus_yr 0 -24 --sx 20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 16 --dimy 32 --res 5 --design_xr -5 5 --design_yr 4 24 --focus_yr 0 -24 --sx 20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 20 --dimy 40 --res 5 --design_xr -5 5 --design_yr 4 24 --focus_yr 0 -24 --sx 20

# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 10 --dimy 5 --res 5 --design_xr -10 10 --design_yr 14 24 --focus_yr 10 -24 --sx 20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 20 --dimy 10 --res 5 --design_xr -10 10 --design_yr 14 24 --focus_yr 10 -24 --sx 20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 30 --dimy 15 --res 5 --design_xr -10 10 --design_yr 14 24 --focus_yr 10 -24 --sx 20
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 40 --dimy 20 --res 5 --design_xr -10 10 --design_yr 14 24 --focus_yr 10 -24 --sx 20

# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 20 --dimy 5 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 10 -24 --sx 40
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 40 --dimy 10 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 10 -24 --sx 40
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 60 --dimy 15 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 10 -24 --sx 40

# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 20 --dimy 10 --res 5 --design_xr -20 20 --design_yr 4 24 --focus_yr 0 -24 --sx 40
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 40 --dimy 20 --res 5 --design_xr -20 20 --design_yr 4 24 --focus_yr 0 -24 --sx 40
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 60 --dimy 30 --res 5 --design_xr -20 20 --design_yr 4 24 --focus_yr 0 -24 --sx 40

# for f in ./output/base/*.h5; do ./plot_results.py -f $f -r 20 -s ./plots/base/; done

##########
## DID NOT RUN
#

# # try to run this if there is time
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 80 --dimy 20 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 13.5 -24 --sx 40
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 80 --dimy 40 --res 5 --design_xr -20 20 --design_yr 4 24 --focus_yr 3.5 -24 --sx 40
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 80 --dimy 20 --res 5 --design_xr -20 20 --design_yr 14 24 --focus_yr 10 -24 --sx 40
# mpiexec $MPIARGS optimize_bsw_mpi.py --dimx 80 --dimy 40 --res 5 --design_xr -20 20 --design_yr 4 24 --focus_yr 0 -24 --sx 40

# # toggle with togglemargin = 4
# for f in ./output/base/*.h5; do
#     mpiexec $MPIARGS optimize_toggle.py --infile $f;
# done

# for f in ./output/toggle/*.h5; do ./plot_results.py -f $f -r 20 -s ./plots/toggle/; done
