# `make clean` removes all derived data. Be careful what you wish for.
# You can create less disruptive clean rules here

clean :
	rm -rf */*.mod */*.f90 */*.o */*.lo */*.vg */*.evx */*.phs */*.log */*.lhe */*.hepmc
	rm -rf */*.olp_parameters */fort.* */stability_log */test_sudakov_data
	rm -rf */*.olp */*.olc */*.la */Generated_Loops */*olp_modules */*.so */lib
	rm -rf */include */.libs/ */fort.7 */golem.in */Gosam_Makefile */*makefile
	rm -rf */gmon.out */*.dat */*.yoda */plots */gosam.crashed
	rm whizard/*_lo-[0-9] -rf
	rm whizard/*_nlo-[0-9] -rf
