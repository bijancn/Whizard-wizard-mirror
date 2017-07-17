#===================#
#  generator label  #
#===================#
 BEGIN SPECIAL /WHIZARD_.*
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.1,0.1){\color{gray}\textsc{Whizard+OpenLoops}}
\endpsclip
 END SPECIAL

#====================#
#  general settings  #
#====================#
 BEGIN PLOT /WHIZARD_.*
LogY=0
RatioPlotYLabel=$\sigma/\sigma^\text{NLO}$
RatioPlotSameStyle=1
LegendYPos=0.99
LegendXPos=0.60
YLabel=$\frac{d\sigma}{d\mathcal{O}}[\text{fb}/[a.u.]]$
 END PLOT

 BEGIN HISTOGRAM /WHIZARD_.*
ErrorBars=0
ErrorBands=0
 END HISTOGRAM

#==========#
#  titles  #
#==========#
 BEGIN PLOT /WHIZARD_.*
Title=$\quad e^+e^-\to t\bar{t}, \quad \quad \sqrt{s} = 500\, \text{GeV}$
 END PLOT

#========================#
#  invariant mass plots  #
#========================#
 BEGIN PLOT /WHIZARD_.*/jets-inv
XLabel=$m(p^{j_1}+p^{j_2})$
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
LegendYPos=0.99
LegendXPos=0.05
 END PLOT

 BEGIN PLOT /WHIZARD_.*/tt-inv
XLabel=$m(p^{t}+p^{\bar{t}})$
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
LegendYPos=0.99
LegendXPos=0.05
XMax=505
LogY=1
RatioPlotYMin=0.2
RatioPlotYMax=10.0
YMin=0.01
 END PLOT

 BEGIN PLOT /WHIZARD_.*/tbarH-inv
XLabel=$m(p^{\bar{t}} + p^H)$
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
LegendYPos=0.99
LegendXPos=0.05
 END PLOT

 BEGIN PLOT /WHIZARD_.*/th-inv
XLabel=$m(p^{t}+p^{H})$
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
LegendYPos=0.99
LegendXPos=0.05
 END PLOT

 BEGIN PLOT /WHIZARD_.*/leading-jet-Theta
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
XLabel=$\cos{\theta^{j_1}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-Theta
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
XLabel=$\cos{\theta^{j_2}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/top-theta
YLabel=$\frac{d\sigma}{d\cos\theta}[\text{fb}/\text{GeV}]$
XLabel=$\cos{\theta^{t}}$
LegendYPos=0.99
LegendXPos=0.60
RatioPlotYMin=0.8
RatioPlotYMax=1.2
 END PLOT

 BEGIN PLOT /WHIZARD_.*/antitop-theta
YLabel=$\frac{d\sigma}{d\cos\theta}[\text{fb}/\text{GeV}]$
XLabel=$\cos{\theta^{\bar{t}}}$
LegendYPos=0.99
LegendXPos=0.05
RatioPlotYMin=0.8
RatioPlotYMax=1.2
 END PLOT



#============#
#  pT plots  #
#============#
 BEGIN PLOT /WHIZARD_.*/.*-pT
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/top-pT
XLabel=$p_T^{t}[\text{GeV}]$
LegendYPos=0.99
LegendXPos=0.05
RatioPlotYMax=1.5
 END PLOT

 BEGIN PLOT /WHIZARD_.*/antitop-pT
XLabel=$p_T^{\bar{t}}[\text{GeV}]$
LegendYPos=0.99
LegendXPos=0.05
RatioPlotYMax=1.5
 END PLOT


 BEGIN PLOT /WHIZARD_.*/leading-jet-pT
XLabel=$p_T^{j_1}[\text{GeV}]$
LegendYPos=0.99
LegendXPos=0.05
RatioPlotYMin=0.6
RatioPlotYMax=1.5
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-pT
XLabel=$p_T^{j_2}[\text{GeV}]$
LegendYPos=0.99
LegendXPos=0.05
RatioPlotYMin=0.2
RatioPlotYMax=1.5
 END PLOT

#===========#
#  E plots  #
#===========#
 BEGIN PLOT /WHIZARD_.*/.*-E
YLabel=$\frac{d\sigma}{dE}[\text{fb}/\text{GeV}]$
LegendXPos=0.05
 END PLOT

 BEGIN PLOT /WHIZARD_.*/top-E
XLabel=$E^{t}[\text{GeV}]$
LogY=1
RatioPlotYMin=0.2
RatioPlotYMax=10.0
YMin=0.01
 END PLOT

 BEGIN PLOT /WHIZARD_.*/antitop-E
XLabel=$E^{\bar{t}}[\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/leading-jet-E
XLabel=$E^{j_1}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-E
XLabel=$E^{j_2}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Higgs-E
XLabel=$E^{H}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/gluon-E
XLabel=$E^{g}[\text{GeV}]$
LogY=1
LegendXPos=0.60
LegendYPos=0.99
XMax=150
RatioPlotYMin=0.2
RatioPlotYMax=10.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/gluon-E-zoom
XLabel=$E^{g}[\text{GeV}]$
LogY=1
LegendXPos=0.60
LegendYPos=0.99
XMax=20
RatioPlotYMin=0.5
RatioPlotYMax=3.0
 END PLOT


#===============#
#  other plots  #
#===============#
 BEGIN PLOT /WHIZARD_.*/jet-count
YLabel=$\frac{d\sigma}{dN_\text{jets}}[\text{fb}]$
XLabel=$N_\text{jets}$
XMax=5.25
XMin=1.25
 END PLOT

