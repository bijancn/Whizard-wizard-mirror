whizard/%.lhe : whizard/%.sin
	cd whizard && $(WHIZARD_BIN) $(WHIZARD_OPTIONS) $(notdir $<)

environment: export WHIZARD_THREADS = $(WHIZ_THREADS)

whizard/%.hepmc : whizard/%.sin
	python ../parallelizer.py $(WHIZARD_BIN) $<
	#cd whizard && $(WHIZARD_BIN) $(WHIZARD_OPTIONS) $(notdir $<)
	mv $(basename $@)-*/*.hepmc rivet/

pythia/%.hepmc : whizard/%.lhe
	cd pythia && ./$(basename $(notdir $@))
	rsync -avz --progress --update $@ rivet/
