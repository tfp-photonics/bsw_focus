#!/bin/bash

#MSUB -l nodes=12:ppn=28
#MSUB -l walltime=24:00:00
#MSUB -l pmem=4000mb
#MSUB -v MPIRUN_OPTIONS="--bind-to core --map-by core -print-rank-map -envall"
#MSUB -v EXE=./optimize_bsw_mpi.py
#MSUB -N OPTIMIZE_BSW_MPI_70x70

module load mpi/impi/5.1.3-intel-16.0
export PATH=$HOME/.virtualenvs/meep-serial/bin:$PATH

startexe="mpirun ${MPIRUN_OPTIONS} ${EXE} --dim 70 --res 6 --matfile 70x70.npy"
echo $startexe
exec $startexe
