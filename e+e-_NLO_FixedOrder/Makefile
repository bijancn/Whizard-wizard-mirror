SHELL:=/bin/bash -O extglob
#WHIZARD_BIN=/scratch/whizard_git/whizard_run_gfortran/bin/whizard
WHIZARD_OPTIONS=--rebuild-events 
HEPMCS=whizard/bbww_lo.hepmc \
	whizard/bbww_nlo.hepmc

all : $(HEPMCS)
	cd rivet && make

include ../buildrules.mk
include ../cleanrules.mk
