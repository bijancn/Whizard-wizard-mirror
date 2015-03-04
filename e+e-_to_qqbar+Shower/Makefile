SHELL:=/bin/bash -O extglob
#WHIZARD_BIN=/scratch/whizard_git/whizard_run_gfortran/bin/whizard
WHIZARD_OPTIONS=--rebuild-events 
HEPMCS=pythia/whizard_uu_lo.hepmc \
	pythia/whizard_uu_powheg.hepmc \
	whizard/whizard_analytic.hepmc

all : $(HEPMCS)
	rsync -v !(rivet)/*.hepmc rivet && cd rivet && make

whizard/%.lhe : whizard/%.sin
	cd whizard && $(WHIZARD_BIN) $(WHIZARD_OPTIONS) $(notdir $<)

whizard/%.hepmc : whizard/%.sin
	cd whizard && $(WHIZARD_BIN) $(WHIZARD_OPTIONS) $(notdir $<)

pythia/%.hepmc : whizard/%.lhe
	cd pythia && ./$(basename $(notdir $@))

clean :
	rm -rf */*.mod */*.f90 */*.o */*.lo */*.vg */*.evx */*.phs */*.log */*.lhe */*.hepmc
	rm -rf */*.olp */*.olc */*.la */Generated_Loops */*olp_modules */*.so */lib
	rm -rf */include */.libs/ */fort.7 */golem.in */Gosam_Makefile */*makefile
