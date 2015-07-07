SHELL:=/bin/bash -O extglob
#WHIZARD_BIN=/scratch/whizard_git/whizard_run_gfortran/bin/whizard
WHIZARD_OPTIONS=--rebuild-events 
HEPMCS=whizard/proc_lo.hepmc \
	whizard/proc_nlo.hepmc

all : $(HEPMCS)
	cd rivet && scons -j10

include ../buildrules.mk
include ../cleanrules.mk
