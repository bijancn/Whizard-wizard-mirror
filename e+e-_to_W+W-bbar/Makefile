SHELL:=/bin/bash -O extglob
#WHIZARD_BIN=/scratch/whizard_git/whizard_run_gfortran/bin/whizard
WHIZARD_OPTIONS=--rebuild-events 
SCAN=whizard/integrate.log

all : $(SCAN)

whizard/%.log : whizard/%.sin
	cd whizard && $(WHIZARD_BIN) $(WHIZARD_OPTIONS) $(notdir $<)

clean :
	rm -rf */*.mod */*.f90 */*.o */*.lo */*.vg */*.evx */*.phs */*.log */*.lhe */*.hepmc
	rm -rf */*.ps */*.aux */*.dvi */*.toc */*.tex */*.out
	rm -rf */*.olp */*.olc */*.la */Generated_Loops */*olp_modules */*.so */lib
	rm -rf */include */.libs/ */fort.7 */golem.in */Gosam_Makefile */*makefile
