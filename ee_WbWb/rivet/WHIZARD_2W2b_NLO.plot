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
LogY=1
RatioPlotYLabel=K-Factor
RatioPlotSameStyle=1
LegendXPos=0.70
YLabel=$\frac{d\sigma}{d\mathcal{O}}[\text{fb}/[a.u.]]$
 END PLOT

 BEGIN HISTOGRAM /WHIZARD_.*
ErrorBars=0
ErrorBands=0
 END HISTOGRAM

#==========#
#  titles  #
#==========#
 BEGIN PLOT /WHIZARD_2W2b_NLO
Title=$\quad e^+e^-\to W^+b W^-\bar{b}$, $N_\text{jets}\geq 2, \quad \quad \sqrt{s} = 800 \text{GeV}$
 END PLOT

 BEGIN PLOT /WHIZARD_2W2b_NLO_ttbarcuts
Title=$\quad e^+e^-\to W^+b W^-\bar{b}$, $N_\text{jets}\geq 2$, $\lvert m_{Wj_b}-m_t\rvert\leq 5 \text{GeV}$
 END PLOT

#========================#
#  invariant mass plots  #
#========================#
 BEGIN PLOT /WHIZARD_.*/.*-inv
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jets-inv*
XLabel=$m(p^{j_1}+p^{j_2})$
RatioPlotYMax=1.5
RatioPlotYMin=0.3
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BW-inv
XLabel=$m^{BW}[\text{GeV}]$
RatioPlotYMax=5.0
RatioPlotYMin=0.65
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BW-inv-peak
XLabel=$m^{BW}[\text{GeV}]$
RatioPlotYMax=5.0
RatioPlotYMin=0.5
LegendXPos=0.15
LegendYPos=0.9
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-inv-Hpeak
XLabel=$m^{bb}[\text{GeV}]$
RatioPlotYMax=5.0
RatioPlotYMin=0.65
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-inv-Zpeak
XLabel=$m^{bb}[\text{GeV}]$
RatioPlotYMax=5.0
RatioPlotYMin=0.65
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-inv
XLabel=$m^{BB}[\text{GeV}]$
RatioPlotYMax=5.0
RatioPlotYMin=0.65
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-inv
XLabel=$m^{BW^-}[\text{GeV}]$
RatioPlotYMax=12.0
RatioPlotYMin=0.5
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-inv-peak
XLabel=$m^{BW^-}[\text{GeV}]$
RatioPlotYMax=5.0
RatioPlotYMin=0.5
LegendXPos=0.8
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-inv
XLabel=$m^{BW^+}[\text{GeV}]$
RatioPlotYMax=12.0
RatioPlotYMin=0.5
LegendXPos=0.8
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-inv-peak
XLabel=$m^{BW^+}[\text{GeV}]$
RatioPlotYMax=5.0
RatioPlotYMin=0.5
LegendXPos=0.8
 END PLOT

#============#
#  pT plots  #
#============#
 BEGIN PLOT /WHIZARD_.*/.*-pT
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/leading-jet-pT
XLabel=$p_T^{j_1}[\text{GeV}]$
RatioPlotYMax=1.6
RatioPlotYMin=0.25
RatioPlotXMax=325.0
XMax=325.0
LegendXPos=0.815
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-pT
XLabel=$p_T^{j_2}[\text{GeV}]$
RatioPlotYMax=1.4
RatioPlotYMin=0.3
RatioPlotXMax=275.0
XMax=275.0
LegendXPos=0.815
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-jet-pT
XLabel=$p_T^{b}[\text{GeV}]$
RatioPlotYMax=1.4
RatioPlotYMin=0.3
 END PLOT

 BEGIN PLOT /WHIZARD_.*/bbar-jet-pT
XLabel=$p_T^{\bar{b}}[\text{GeV}]$
RatioPlotYMax=1.4
RatioPlotYMin=0.3
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wp-pT
XLabel=$p_T^{W^+}[\text{GeV}]$
RatioPlotYMax=1.3
RatioPlotYMin=0.3
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wm-pT
XLabel=$p_T^{W^-}[\text{GeV}]$
RatioPlotYMax=1.3
RatioPlotYMin=0.3
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-pT
XLabel=$p_T^{bb}[\text{GeV}]$
RatioPlotYMax=1.3
RatioPlotYMin=0.3
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-pT
XLabel=$p_T^{\bar{b}W^-}[\text{GeV}]$
RatioPlotYMax=1.5
RatioPlotYMin=0.3
RatioPlotXMax=360.0
XMax=360.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-pT
XLabel=$p_T^{bW^+}[\text{GeV}]$
RatioPlotYMax=1.5
RatioPlotYMin=0.3
RatioPlotXMax=360.0
XMax=360.0
 END PLOT


#===========#
#  E plots  #
#===========#
 BEGIN PLOT /WHIZARD_.*/.*-E
YLabel=$\frac{d\sigma}{dE}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/leading-jet-E
XLabel=$E^{j_1}[\text{GeV}]$
RatioPlotYMax=2.35
RatioPlotYMin=0.35
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-E
XLabel=$E^{j_2}[\text{GeV}]$
RatioPlotYMax=2.35
RatioPlotYMin=0.35
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-jet-E
XLabel=$E^{b}[\text{GeV}]$
RatioPlotYMax=2.5
RatioPlotYMin=0.5
 END PLOT

 BEGIN PLOT /WHIZARD_.*/bbar-jet-E
XLabel=$E^{\bar{b}}[\text{GeV}]$
RatioPlotYMax=2.5
RatioPlotYMin=0.5
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wp-E
XLabel=$E^{W^+}[\text{GeV}]$
RatioPlotYMax=1.55
RatioPlotYMin=0.35
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wm-E
XLabel=$E^{W^-}[\text{GeV}]$
RatioPlotYMax=1.55
RatioPlotYMin=0.35
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-E
XLabel=$E^{b\bar{b}}[\text{GeV}]$
RatioPlotYMax=1.8
RatioPlotYMin=0.3
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-E
XLabel=$E^{bW^-}[\text{GeV}]$
RatioPlotYMax=7.0
RatioPlotYMin=0.05
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-E
XLabel=$E^{\bar{b}W^+}[\text{GeV}]$
RatioPlotYMax=7.0
RatioPlotYMin=0.05
 END PLOT

#=========================#
#  angular distributions  #
#=========================#

 BEGIN PLOT /WHIZARD_.*/.*-Theta
YLabel=$\frac{d\sigma}{d\cos\theta}[\text{fb}/\text{GeV}]$
LegendXPos=0.8
LagendYPos=0.9
 END PLOT

 BEGIN PLOT /WHIZARD_.*/leading-jet-Theta
XLabel=$\cos\theta^{j_1}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-Theta
XLabel=$\cos\theta^{j_2}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-Theta
XLabel=$\cos\theta^{b\bar{b}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-Theta
XLabel=$\cos\theta^{\bar{b}W^-}$
YLabel=$\frac{d\sigma}{d\cos\theta}[\text{fb}]$
LegendXPos=0.1
RatioPlotYMin=0.8
RatioPlotYMax=1.2
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-Theta
XLabel=$\cos\theta^{bW^+}$
YLabel=$\frac{d\sigma}{d\cos\theta}[\text{fb}]$
LegendXPos=0.75
RatioPlotYMin=0.8
RatioPlotYMax=1.2
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wm-Theta
XLabel=$\cos\theta^{W^-}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wp-Theta
XLabel=$\cos\theta^{W^+}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-jet-Theta
XLabel=$\cos\theta^{b}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/bbar-jet-Theta
XLabel=$\cos\theta^{\bar{b}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-jet-Theta
XLabel=$\cos\theta^{b}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Phi\(b\,Wm\)
YLabel=$\frac{d\sigma}{d\phi}[\text{fb}/\text{GeV}]$
XLabel=$\phi^{\bar{b}W^-}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Phi\(b\,Wp\)
YLabel=$\frac{d\sigma}{d\phi}[\text{fb}/\text{GeV}]$
XLabel=$\phi^{bW^+}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Phi\(b\,b\)
YLabel=$\frac{d\sigma}{d\phi}[\text{fb}/\text{GeV}]$
XLabel=$\phi^{b\bar{b}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Phi\(b\,Wm\)
YLabel=$\frac{d\sigma}{d\phi}[\text{fb}/\text{GeV}]$
XLabel=$\phi^{\bar{b}W^-}$
 END PLOT

#==================#
#  rapidity plots  #
#==================#
 BEGIN PLOT /WHIZARD_.*/R\(b\,Wm\)
YLabel=$\frac{d\sigma}{dR}[\text{fb}/\text{GeV}]$
XLabel=$R^{\bar{b}W^-}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/R\(b\,Wp\)
YLabel=$\frac{d\sigma}{dR}[\text{fb}/\text{GeV}]$
XLabel=$R^{bW^+}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/R\(b\,b\)
YLabel=$\frac{d\sigma}{dR}[\text{fb}/\text{GeV}]$
XLabel=$R^{b\bar{b}}$
 END PLOT

#===============#
#  other plots  #
#===============#

 BEGIN PLOT /WHIZARD_.*/jet-count
YLabel=$\frac{d\sigma}{dN_\text{jets}}[\text{fb}]$
XLabel=$N_\text{jets}$
 END PLOT

