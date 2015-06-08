whizard/%.lhe : whizard/%.sin
	cd whizard && $(WHIZARD_BIN) $(WHIZARD_OPTIONS) $(notdir $<)

whizard/%.hepmc : whizard/%.sin
	cd whizard && $(WHIZARD_BIN) $(WHIZARD_OPTIONS) $(notdir $<)
	rsync -avz --progress --update $@ rivet/

pythia/%.hepmc : whizard/%.lhe
	cd pythia && ./$(basename $(notdir $@))
	rsync -avz --progress --update $@ rivet/
