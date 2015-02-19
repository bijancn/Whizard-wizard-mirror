# Tip: export RIVET_ANALYSIS_PATH=$PWD or use --pwd
# For new template: rivet-mkanalysis WHIZARD_*

hepfile=test.hepmc
yodafile=Rivet.yoda
ANALYIS=WHIZARD_2015_SINGLEEMISSION

all: plots/index.html

RivetAnalysis.so: *.cc
	rivet-buildplugin *.cc

Rivet.yoda: RivetAnalysis.so $(hepfile)
	rivet --analysis $(ANALYIS) $(hepfile)

debug: RivetAnalysis.so $(hepfile)
	rivet --analysis $(ANALYIS) $(hepfile) -l Rivet.Analysis=DEBUG -n 5

plots/index.html: $(yodafile)
	rivet-mkhtml $(yodafile)

clean:
	rm *.so *.yoda plots -rf
