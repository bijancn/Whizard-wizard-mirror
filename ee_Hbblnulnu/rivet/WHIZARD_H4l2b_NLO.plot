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
 BEGIN PLOT /WHIZARD_.*
Title=$\quad e^+e^-\to \mu^+\nu_\mu e^-\bar{\nu_e} b \bar{b} H$, $N_\text{jets}\geq 2, \quad \quad \sqrt{s} = 800 \text{GeV}$
 END PLOT

#========================#
#  invariant mass plots  #
#========================#
 BEGIN PLOT /WHIZARD_.*/.*-inv
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jets-inv
XLabel=$m^{j_1,j_2}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jets-inv-Hpeak
XLabel=$m^{j_1,j_2}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jets-inv-Zpeak
XLabel=$m^{j_1,j_2}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/WW-inv
XLabel=$m^{WW}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-inv
XLabel=$m^{BW^+}[\text{GeV}]$
RatioPlotYMax=12.0
RatioPlotYMin=0.65
LegendXPos=0.25
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-inv
XLabel=$m^{BW^-}[\text{GeV}]$
RatioPlotYMax=12.0
RatioPlotYMin=0.65
LegendXPos=0.25
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWpBWp-inv
XLabel=$m^{BBW^+W^-}[\text{GeV}]$
LegendXPos=0.45
LegendYPos=0.45
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWpH-inv
XLabel=$m^{HBW^+}[\text{GeV}]$
LegendXPos=0.25
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BW-inv-peak
XLabel=$m^{BW}[\text{GeV}]$
LegendXPos = 0.8
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BW-inv
XLabel=$m^{BW}[\text{GeV}]$
LegendXPos = 0.8
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-inv-*
XLabel=$m^{BB}[\text{GeV}]$
XMax=550.0
RatioPlotXMax=550.0
RatioPlotYMax=2.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Bl-inv-*
LogY=0
XLabel=$m^{Bl}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blm-inv-*
XLabel=$m^{Bl^-}[\text{GeV}]$
XMax=200.0
RatioPlotXMax=200.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blp-inv-*
XLabel=$m^{Bl^+}[\text{GeV}]$
XMax=200.0
RatioPlotXMax=200.0
LegendXPos=0.81
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BlpBlp-inv-*
XLabel=$m^{BBl^-l^+}[\text{GeV}]$
LegendXPos=0.81
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BlpH-inv-*
XLabel=$m^{BHl^+}[\text{GeV}]$
LegendXPos=0.81
 END PLOT

 BEGIN PLOT /WHIZARD_.*/W-inv-peak
XLabel=$m^W[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/W-inv
XLabel=$m^W[\text{GeV}]$
 END PLOT

#============#
#  pT plots  #
#============#
 BEGIN PLOT /WHIZARD_.*/.*-pT
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jet-pT
XLabel=$\sum_i p_T^{j_i}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/gluon-pT
XLabel=$p_{T,g}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-quark-pT
XLabel=$p_{T,b}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/leading-jet-pT
XLabel=$p_T^{j_1}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
XMax=350.0
RatioPlotXMax=350.0
LegendXPos=0.815
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-pT
XLabel=$p_T^{j_2}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
LegendXPos=0.815
XMax=200.0
RatioPlotXMax=200.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-jet-pT
XLabel=$p_T^{b}[\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/bbar-jet-pT
XLabel=$p_T^{\bar{b}}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/hardest-lepton-pT
XLabel=$p_T^{l_1}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-hardest-lepton-pT
XLabel=$p_T^{l_2}[\text{GeV}]$
XMax=200.0
RatioPlotXMax=200.0
 END PLOT


 BEGIN PLOT /WHIZARD_.*/W_plus-pT
XLabel=$p_{T,W^+}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-pT
XLabel=$p_T^{BB}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
XMax=350.0
RatioPlotXMax=350.0
LegendXPos=0.8
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-pT
XLabel=$p_T^{BW^-}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
XMax=350.0
RatioPlotXMax=350.0
RatioPlotYMax=1.3
RatioPlotYMin=0.3
LegendYPos=0.75
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-pT
XLabel=$p_T^{BW^+}[\text{GeV}]$
XMax=325.0
RatioPlotXMax=325.0
RatioPlotYMax=1.3
RatioPlotYMin=0.3
LegendYPos=0.75
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWpBWm-pT
XLabel=$p_T^{BBW^+W^-}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWpH-pT
XLabel=$p_T^{HBW^+}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blm-pT
XLabel=$p_T^{Bl^-}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
XMax=325.0
RatioPlotXMax=325.0
RatioPlotYMax=1.25
RatioPlotYMin=0.65
LegendYPos=0.75
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blp-pT
XLabel=$p_T^{Bl^+}[\text{GeV}]$
XMax=325.0
RatioPlotXMax=325.0
RatioPlotYMax=1.25
RatioPlotYMin=0.65
LegendYPos=0.75
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BlpBlm-pT
XLabel=$p_T^{BBl^+l^-}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BlpH-pT
XLabel=$p_T^{BHl^+}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/Wm-pT
XLabel=$p_T^{W^-}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wp-pT
XLabel=$p_T^{W^+}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/electron-Pt
XLabel=$p_T^{e^-}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
XMax=350.0
RatioPlotXMax=350.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/muon-Pt
XLabel=$p_T^{\mu^+}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
XMax=350.0
RatioPlotXMax=350.0
 END PLOT


 BEGIN PLOT /WHIZARD_.*/lepton-lepton-Pt
XLabel=$p_T^{ll}[\text{GeV}]$
 END PLOT










#===========#
#  E plots  #
#===========#
 BEGIN PLOT /WHIZARD_.*/.*-E$
YLabel=$\frac{d\sigma}{dE}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/leading-jet-E
XLabel=$E^{j_1}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-E
XLabel=$E^{j_2}[\text{GeV}]$
XMax=250.0
RatioPlotXMax=250.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-jet-E
XLabel=$E^{b}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/hardest-lepton-E
XLabel=$E^{l_1}[\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/2nd-hardest-lepton-E
XLabel=$E^{l_2}[\text{GeV}]$
XMax=250.0
RatioPlotXMax=250.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-E
XLabel=$E^{BB}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/gluon-E
XLabel=$E_g[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/W_plus-E
XLabel=$E_{W^+}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/W_plus-E
XLabel=$E_{W^+}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-E
XLabel=$E^{BW^-}[\text{GeV}]$
LegendXPos=0.25
RatioPlotYMax=60
RatioPlotYMin=0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-E
XLabel=$E^{BW^+}[\text{GeV}]$
XMax=375.0
RatioPlotXMax=375.0
RatioPlotYMax=60
RatioPlotYMin=0
LegendXPos=0.25
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blp-E
XLabel=$E^{Bl^+}[\text{GeV}]$
XMax=375.0
RatioPlotXMax=375.0
RatioPlotYMax=0
RatioPlotYMin=60
LegendXPos=0.75
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blm-E
XLabel=$E^{Bl^-}[\text{GeV}]$
XMax=400.0
RatioPlotXMax=400.0
RatioPlotYMax=0
RatioPlotYMin=60
LegendXPos=0.75
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BlpBlm-E
XLabel=$E^{BBl^+l^-}[\text{GeV}]$
LegendXPos=0.8
RatioPlotYMin=0.6
RatioPlotYMax=2.5
LegendXPos=0.85
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BlpH-E
XLabel=$E^{BHl^+}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWpBWm-E
XLabel=$E^{BBW^+W^-}[\text{GeV}]$
LegendXPos=0.25
RatioPlotYMin=0.25
RatioPlotYMax=2.5
LegendXPos=0.45
LegendYPos=0.45
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWpH-E
XLabel=$E^{HBW^+}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wm-E
XLabel=$E^{W^-}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wp-E
XLabel=$E^{W^+}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/electron-E
XLabel=$E^{e^-}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/muon-E
XLabel=$E^{\mu^+}[\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/lepton-lepton-E
XLabel=$E^{ll}[\text{GeV}]$
 END PLOT



 BEGIN PLOT /WHIZARD_.*/Wm-inv
XLabel=$m^{W^-}[\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/Wm-inv-peak
XLabel=$m^{W^-}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wp-inv
XLabel=$m^{W^+}[\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/Wp-inv-peak
XLabel=$m^{W^+}[\text{GeV}]$
 END PLOT




#===============#
#  angle plots  #
#===============#
 BEGIN PLOT /WHIZARD_.*-Theta
YLabel=$\frac{d\sigma}{d{\cos{\theta}}}$[fb]
LegendXPos=0.8
LegendYPos=0.9
Rebin=8
 END PLOT

 BEGIN PLOT /WHIZARD_.*Phi*
YLabel=$\frac{d\sigma}{d\phi}[\text{fb}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*Phi\(b\,Wm\)
XLabel=$\phi^{BW^-}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*Phi\(b\,Wp\)
XLabel=$\phi^{BW^+}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*Phi\(b\,b\)
XLabel=$\phi^{BB}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*Phi\(b\,lm\)
XLabel=$\phi^{Bl^-}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*Phi\(b\,lp\)
XLabel=$\phi^{Bl^+}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*Phi\(l\+\,l\-\)
XLabel=$\phi^{l^+l^-}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*Phi\(l\-\,MET\)
LegendXPos=0.5
 END PLOT



 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-Theta
XLabel=$\cos\theta^{j_2}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-Theta
XLabel=$\cos\theta^{BB}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-Theta
XLabel=$\cos\theta^{BW^+}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-Theta
XLabel=$\cos\theta^{BW^-}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blm-Theta
XLabel=$\cos\theta^{Bl^-}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blp-Theta
XLabel=$\cos\theta^{Bl^+}$
 END PLOT






 BEGIN PLOT /WHIZARD_.*R\(b\,Wm\)
YLabel=$\frac{d\sigma}{dR}[\text{fb}]$
XLabel=$R^{BW^-}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*R\(b\,Wp\)
YLabel=$\frac{d\sigma}{dR}[\text{fb}]$
XLabel=$R^{BW^+}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*R\(b\,b\)
YLabel=$\frac{d\sigma}{dR}[\text{fb}]$
XLabel=$R^{BB}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*R\(b\,lm\)
YLabel=$\frac{d\sigma}{dR}[\text{fb}]$
XLabel=$R^{Bl^-}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*R\(b\,lp\)
YLabel=$\frac{d\sigma}{dR}[\text{fb}]$
XLabel=$R^{Bl^+}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*R\(l\+\,l\-\)
YLabel=$\frac{d\sigma}{dR}[\text{fb}]$
XLabel=$R^{l^+l^-}$
 END PLOT

#===============#
#  rapidity plots  #
#===============#
 BEGIN PLOT /WHIZARD_.*-Eta
YLabel=$\frac{d\sigma}{d{\cos{\eta}}}$[fb]
 END PLOT

 BEGIN PLOT /WHIZARD_.*electron-Eta
XLabel=$\eta^{e^-}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*muon-Eta
XLabel=$\eta^{\mu^+}$
 END PLOT


 BEGIN PLOT /WHIZARD_.*hardest-lepton-Eta
XLabel=$\eta^{l_1}$
 END PLOT

#===============#
#  Higgs plots  #
#===============#
 BEGIN PLOT /WHIZARD_.*/Higgs-E
YLabel=$\frac{d\sigma}{dE}$[fb]
XLabel=$E^H$[fb]
LegendXPos=0.25
RatioPlotYMin=0.8
RatioPlotYMax=2.5
LegendXPos=0.45
LegendYPos=0.45
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Higgs-Pt
YLabel=$\frac{d\sigma}{dp_T}$[fb]
XLabel=$p_T^H$[fb]
LegendXPos=0.25
RatioPlotYMin=0.8
RatioPlotYMax=2.5
LegendXPos=0.45
LegendYPos=0.45
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Higgs-Theta
YLabel=$\frac{d\sigma}{d\cos\theta}$[fb]
XLabel=$\cos\theta^H$[fb]
 END PLOT


#===============#
#  other plots  #
#===============#

 BEGIN PLOT /WHIZARD_.*/MET
YLabel=$\frac{d\sigma}{dE_T^{\text{miss}}}$[fb]
XLabel=$E_T^{\text{miss}}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/MPT
YLabel=$\frac{d\sigma}{d{p_T^{\text{miss}}}}$[fb]
XLabel=$p_T^{\text{miss}}[\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/jet-count
YLabel=$\frac{d\sigma}{dN_\text{jets}}[\text{fb}]$
XLabel=$N_\text{jets}$
 END PLOT

