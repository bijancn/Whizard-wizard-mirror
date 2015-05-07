# Tip: export RIVET_ANALYSIS_PATH=$PWD or use --pwd
# For new template: rivet-mkanalysis WHIZARD_*
#
# yodamerge -o Rivet.yoda $(YODAFILES) combines multiple yoda files to one
# (adding statistics etc.)
# yodafile=Rivet.yoda

yodafiles=nlo_powheg_500K.yoda lo_pythia_1emission_500k.yoda
hepfile=nlo_powheg_500K.hepmc
ANALYSIS=WHIZARD_2015_SINGLEEMISSION

all: plots/index.html

RivetAnalysis.so: *.cc
	rivet-buildplugin *.cc

$(yodafiles): RivetAnalysis.so

%.yoda: %.hepmc
	rivet --pwd -a $(ANALYSIS) -H $@ $< -q

debug: RivetAnalysis.so
	rivet --pwd -a $(ANALYSIS) $(hepfile) -l Rivet.Analysis=DEBUG --nevts=5

plots/index.html: $(yodafiles)
	rivet-mkhtml $(yodafiles)

clean:
	rm *.so *.yoda plots -rf
