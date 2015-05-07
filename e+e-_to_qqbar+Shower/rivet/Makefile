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
mini_ana_files = \
	whizard_analytic \
	whizard_analytic_MLM1
mini_ana_desc = \
	$s{LO+AnalyticShower}$e \
	$s{Analytic+MLM}$e
mini_ana = $(join $(mini_ana_files),$(mini_ana_desc))

analytic_files = \
	$(mini_ana_files) \
	whizard_analytic_lamm \
	whizard_analytic_lamp \
	whizard_analytic_lowercutoff
analytic_desc = \
	$(mini_ana_desc) \
	$s{Analytic}$$\alpha_+$$$e \
	$s{Analytic}\;lowercutoff$e \
	$s{Analytic}$$\alpha_-$$$e
analytic = $(join $(analytic_files),$(analytic_desc))
hepmc_ana = $(addsuffix .hepmc,$(analytic_files))

pythia_files = \
	whizard_uu_lo \
	whizard_uu_powheg
pythia_desc = \
	$s{LO+Pythia8}$e \
	$s{Powheg+Pythia8}$e
pythia = $(join $(pythia_files),$(pythia_desc))
hepmc_py = $(addsuffix .hepmc,$(pythia_files))

hepmcfiles = $(hepmc_ana) $(hepmc_py)
yodafiles = $(hepmcfiles:.hepmc=.yoda)

all = $(pythia) $(mini_ana)

yodafile=Rivet.yoda
ANALYSIS=WHIZARD_2015_SINGLEEMISSION

all: plots/index.html pythia/index.html analytic/index.html
	echo $(yodafiles)

RivetAnalysis.so: *.cc
	rivet-buildplugin *.cc

$(yodafiles): RivetAnalysis.so

%.yoda: %.hepmc
	rivet --pwd -a $(ANALYSIS) -H $@ $< -q

debug: RivetAnalysis.so
	rivet --pwd -a $(ANALYSIS) $(hepfile) -l Rivet.Analysis=DEBUG --nevts=5

plots/index.html : $(yodafiles) $(ANALYSIS).info $(ANALYSIS).plot
	rivet-mkhtml --mc-errs --pdf --cm -n $N -s -o $(dir $@) $(all)

pythia/index.html : $(yodafiles) $(ANALYSIS).info $(ANALYSIS).plot
	rivet-mkhtml --mc-errs --pdf --cm -n $N -s -o $(dir $@) $(pythia)

analytic/index.html : $(yodafiles) $(ANALYSIS).info $(ANALYSIS).plot
	rivet-mkhtml --mc-errs --pdf --cm -n $N -s -o $(dir $@) $(analytic)

dist:
	rsync -avz @(analytic|plots|pythia) /data/bcho/BitPocketMaster/

clean:
	rm *.so *.yoda plots -rf
