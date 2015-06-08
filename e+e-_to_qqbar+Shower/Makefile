SHELL:=/bin/bash -O extglob
#WHIZARD_BIN=/scratch/whizard_git/whizard_run_gfortran/bin/whizard
WHIZARD_OPTIONS=--rebuild-events 
HEPMCS=pythia/whizard_uu_lo.hepmc \
	pythia/whizard_uu_powheg.hepmc \
	whizard/whizard_analytic.hepmc \
	whizard/whizard_analytic_lamp.hepmc \
	whizard/whizard_analytic_lamm.hepmc \
	whizard/whizard_analytic_lowercutoff.hepmc

all : $(HEPMCS)
	cd rivet && make

include ../buildrules.mk
include ../cleanrules.mk
