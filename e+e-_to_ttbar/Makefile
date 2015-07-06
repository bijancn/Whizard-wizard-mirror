SHELL:=/bin/bash -O extglob
#WHIZARD_BIN=/scratch/whizard_git/whizard_run_gfortran/bin/whizard
WHIZARD_OPTIONS=--rebuild-events 
HEPMCS=whizard/tt_lo.hepmc \
	whizard/tt_nlo.hepmc

all : $(HEPMCS)
	cd rivet && scons -j

include ../buildrules.mk
include ../cleanrules.mk
