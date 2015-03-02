#WHIZARD_BIN=/scratch/whizard_git/whizard_run_gfortran/bin/whizard
WHIZARD_OPTIONS=--rebuild-events 
HEPMC_FILES=whizard_uu_lo.hepmc whizard_uu_powheg.hepmc

all: $(HEPMC_FILES)
	rsync pythia/*.hepmc rivet && cd rivet && make

%.lhe: %
	cd $< && $(WHIZARD_BIN) $(WHIZARD_OPTIONS) run.sin

%.hepmc: %.lhe
	cd pythia; ./$(<:.lhe=)

clean:
	rm */*.mod */*.f90 */*.o */*.lo *.lhe *.hepmc -f
