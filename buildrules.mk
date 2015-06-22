whizard/%.lhe : whizard/%.sin
	cd whizard && $(WHIZARD_BIN) $(WHIZARD_OPTIONS) $(notdir $<)

whizard/%.hepmc : whizard/%.sin
	python parallelizer.py $(WHIZARD_BIN) $<
	#cd whizard && $(WHIZARD_BIN) $(WHIZARD_OPTIONS) $(notdir $<)
	rsync -avz --progress --update $(basename $@)-*/*.hepmc rivet/

pythia/%.hepmc : whizard/%.lhe
	cd pythia && ./$(basename $(notdir $@))
	rsync -avz --progress --update $@ rivet/
