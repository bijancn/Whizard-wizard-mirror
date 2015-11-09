SHELL:=/bin/bash -O extglob
#WHIZARD_BIN=/scratch/whizard_git/whizard_run_gfortran/bin/whizard
WHIZARD_OPTIONS=--rebuild-events 
HEPMCS=whizard/proc_lo.hepmc \
	whizard/proc_nlo.hepmc
export WHIZARD_THREADS=16
export WHIZARD_BATCHES=16

all : $(HEPMCS)
	cd rivet && scons -j10

include ../buildrules.mk
include ../cleanrules.mk
