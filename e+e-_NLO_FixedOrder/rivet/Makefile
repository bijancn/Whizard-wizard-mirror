# Tip: export RIVET_ANALYSIS_PATH=$PWD or use --pwd
# For new template: rivet-mkanalysis WHIZARD_*
# yodamerge -o Rivet.yoda $(YODAFILES) combines multiple yoda files to one
# (adding statistics etc.)

N = 4
s = .yoda:'Title=\textsc
e = '
# :'ErrorBands=1':'ErrorBandColor=blue' # Can be used for renscale plot
# :'RatioPlotYLabel=Ratio':'RatioPlotSameStyle=1' # Doesnt work
# Warning: You cannot use spaces in the descriptions. Make can't escape them.

pythia_files = \
	bbww_lo \
	bbww_nlo
pythia_desc =
#pythia_desc = \
#	$s{LO+Pythia8}$e \
#	$s{Powheg+Pythia8}$e
pythia = $(join $(pythia_files),$(pythia_desc))
hepmc_py = $(addsuffix .hepmc,$(pythia_files))

hepmcfiles = $(hepmc_ana) $(hepmc_py)
yodafiles = $(hepmcfiles:.hepmc=.yoda)

#all = $(pythia) $(mini_ana)
#all = $(pythia)
all = $(yodafiles)

yodafile=Rivet.yoda
ANALYSIS=WHIZARD_2015_NLO

all: plots/index.html
	echo $(pythia_files) $(yodafiles)

RivetAnalysis.so: *.cc
	rivet-buildplugin *.cc

$(yodafiles): RivetAnalysis.so

%.yoda: %.hepmc
	echo $(pythia_files) $(yodafiles)
	rivet --pwd -a $(ANALYSIS) -H $@ $(basename $<).*.hepmc
	#rivet --pwd -a $(ANALYSIS) -H bbww_lo.yoda bbww_lo.hepmc -q --cross-section=564.89068
	#rivet --pwd -a $(ANALYSIS) -H bbww_nlo.yoda bbww_nlo.hepmc -q --cross-section=478.70303

debug: RivetAnalysis.so
	rivet --pwd -a $(ANALYSIS) $(hepfile) -l Rivet.Analysis=DEBUG --nevts=5

plots/index.html: $(yodafiles) $(ANALYSIS).info $(ANALYSIS).plot
	echo $(pythia_files) $(yodafiles)
	rivet-mkhtml --mc-errs --pdf --cm -s -o $(dir $@) $(all)

dist:
	rsync -avz @(analytic|plots|pythia) /data/bcho/BitPocketMaster/

clean:
	rm *.so *.yoda plots -rf
