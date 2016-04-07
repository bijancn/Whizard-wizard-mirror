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
RatioPlotYLabel=K-Factor
RatioPlotSameStyle=1
LegendYPos=0.90
LegendXPos=0.65
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
Title=$\quad e^+e^-\to t\bar{t}, \quad \quad \sqrt{s} = 800\, \text{GeV}$
 END PLOT

#========================#
#  invariant mass plots  #
#========================#
 BEGIN PLOT /WHIZARD_.*/jets-inv
LogY=1
XLabel=$m(p^{j_1}+p^{j_2})$
LegendYPos=0.90
LegendXPos=0.05
 END PLOT

 BEGIN PLOT /WHIZARD_.*/tt-inv
LogY=1
XLabel=$m(p^{t}+p^{\bar{t}})$
LegendYPos=0.90
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
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
XLabel=$\cos{\theta^{t}}$
LegendYPos=0.90
LegendXPos=0.8
 END PLOT

 BEGIN PLOT /WHIZARD_.*/antitop-theta
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
XLabel=$\cos{\theta^{\bar{t}}}$
LegendYPos=0.90
LegendXPos=0.15
 END PLOT



#============#
#  pT plots  #
#============#
 BEGIN PLOT /WHIZARD_.*/.*-pT
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
LogY=1
 END PLOT

 BEGIN PLOT /WHIZARD_.*/top-pT
XLabel=$p_T^{t}[\text{GeV}]$
LegendYPos=0.90
LegendXPos=0.15
XMax=355.0
RatioPlotXMax=355.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/antitop-pT
XLabel=$p_T^{\bar{t}}[\text{GeV}]$
LegendYPos=0.90
LegendXPos=0.15
 END PLOT


 BEGIN PLOT /WHIZARD_.*/leading-jet-pT
XLabel=$p_T^{j_1}[\text{GeV}]$
LegendYPos=0.90
LegendXPos=0.15
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-pT
XLabel=$p_T^{j_2}[\text{GeV}]$
LegendYPos=0.90
LegendXPos=0.15
 END PLOT

#===========#
#  E plots  #
#===========#
 BEGIN PLOT /WHIZARD_.*/.*-E
YLabel=$\frac{d\sigma}{dE}[\text{fb}/\text{GeV}]$
LegendXPos=0.05
LogY=1
 END PLOT

 BEGIN PLOT /WHIZARD_.*/top-E
XLabel=$E^{t}[\text{GeV}]$
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

#===============#
#  other plots  #
#===============#
 BEGIN PLOT /WHIZARD_.*/jet-count
YLabel=$\frac{d\sigma}{dN_\text{jets}}[\text{fb}]$
XLabel=$N_\text{jets}$
 END PLOT

