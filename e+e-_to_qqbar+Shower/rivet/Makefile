# Tip: export RIVET_ANALYSIS_PATH=$PWD or use --pwd
# For new template: rivet-mkanalysis WHIZARD_*
# yodamerge -o Rivet.yoda $(YODAFILES) combines multiple yoda files to one
# (adding statistics etc.)

hepmcfiles = whizard_uu_lo.hepmc whizard_analytic.hepmc whizard_uu_powheg.hepmc
yodafiles = $(hepmcfiles:.hepmc=.yoda)
labeledyodafiles = \
	whizard_uu_lo.yoda:'Title=\textsc{LO+Pythia8}' \
	whizard_uu_powheg.yoda:'Title=\textsc{Powheg+Pythia8}' \
	whizard_analytic.yoda:'Title=\textsc{LO+AnalyticShower}'

labeledyodafiles_noanalytic = \
	whizard_uu_lo.yoda:'Title=\textsc{LO+Pythia8}' \
	whizard_uu_powheg.yoda:'Title=\textsc{Powheg+Pythia8}'

yodafile=Rivet.yoda
ANALYSIS=WHIZARD_2015_SINGLEEMISSION

all: plots/index.html noanalytic/index.html

RivetAnalysis.so: *.cc
	rivet-buildplugin *.cc

$(yodafiles): RivetAnalysis.so

%.yoda: %.hepmc
	rivet --pwd -a $(ANALYSIS) -H $@ $< -q

debug: RivetAnalysis.so
	rivet --pwd -a $(ANALYSIS) $(hepfile) -l Rivet.Analysis=DEBUG --nevts=5

plots/index.html : $(yodafiles) $(ANALYSIS).info $(ANALYSIS).plot
	rivet-mkhtml --pdf --cm --mc-errs -s -o $(dir $@) $(labeledyodafiles)

noanalytic/index.html : $(yodafiles) $(ANALYSIS).info $(ANALYSIS).plot
	rivet-mkhtml --pdf --cm --mc-errs -s -o $(dir $@) $(labeledyodafiles_noanalytic)

clean:
	rm *.so *.yoda plots -rf
