#===================#
#  generator label  #
#===================#
 BEGIN SPECIAL /WHIZARD_.*
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.1,0.1){\color{gray}\textsc{Whizard+OpenLoops}}
\endpsclip
 END SPECIAL

 BEGIN SPECIAL /WHIZARD_.*/BW-inv-peak
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.25,0.1){\color{gray}\textsc{Whizard+OpenLoops}}
\endpsclip
 END SPECIAL

 BEGIN SPECIAL /WHIZARD_.*/BW-pT
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.2,0.1){\color{gray}\textsc{Whizard+OpenLoops}}
\endpsclip
 END SPECIAL

 BEGIN SPECIAL /WHIZARD_.*/BWp-pT
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.2,0.1){\color{gray}\textsc{Whizard+OpenLoops}}
\endpsclip
 END SPECIAL



#====================#
#  general settings  #
#====================#
 BEGIN PLOT /WHIZARD_.*
LogY=1
Rebin=2
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
Title=$\quad e^+e^-\to \mu^+\nu_\mu e^-\bar{\nu_e} b \bar{b}$, $N_\text{jets}\geq 2, \quad \quad \sqrt{s} = 800\,\text{GeV}$
 END PLOT

#========================#
#  invariant mass plots  #
#========================#
 BEGIN PLOT /WHIZARD_.*/.*-inv
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jets-inv
XLabel=$m_{j_1,j_2}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jets-inv-Hpeak
XLabel=$m_{j_1,j_2}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jets-inv-Zpeak
XLabel=$m_{j_1,j_2}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/WW-inv
XLabel=$m_{WW}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-inv
XLabel=$m_{BW^+}[\text{GeV}]$
RatioPlotYMax=5.0
RatioPlotYMin=0.5
LegendXPos=0.25
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-inv
XLabel=$m_{BW^-}[\text{GeV}]$
RatioPlotYMax=5.0
RatioPlotYMin=0.5
LegendXPos=0.25
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BW-inv-peak
XLabel=$m_{Wj_b}[\text{GeV}]$
RatioPlotYMax=5.0
LegendXPos = 0.15
LegendYPos = 0.9
Rebin=1
 END PLOT



 BEGIN PLOT /WHIZARD_.*/BB-inv-*
XLabel=$m_{BB}[\text{GeV}]$
XMax=550.0
RatioPlotXMax=550.0
RatioPlotYMax=2.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Bl-inv-*
XLabel=$m_{Bl}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blm-inv-*
XLabel=$m_{Bl^-}[\text{GeV}]$
XMax=200.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blp-inv
XLabel=$m_{l^+ j_b}[\text{GeV}]$
XMax=180.0
LegendXPos = 0.05
LegendYPos = 0.9
RatioPlotYMin=0.8
Rebin=1
 END PLOT

 BEGIN PLOT /WHIZARD_.*/W-inv-peak
XLabel=$m_W[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/W-inv
XLabel=$m_W[\text{GeV}]$
 END PLOT

#============#
#  pT plots  #
#============#
 BEGIN PLOT /WHIZARD_.*/.*-pT
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jet-pT
XLabel=$\sum_i p_{T,{j_i}}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/gluon-pT
XLabel=$p_{T,g}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-quark-pT
XLabel=$p_{T,b}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/leading-jet-pT
XLabel=$p_{T,{j_1}}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
XMax=350.0
RatioPlotXMax=350.0
LegendXPos=0.815
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-pT
XLabel=$p_{T,{j_2}}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
LegendXPos=0.815
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-jet-pT
XLabel=$p_{T,{b}}[\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/bbar-jet-pT
XLabel=$p_{T,{\bar{b}}}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/hardest-lepton-pT
XLabel=$p_{T,{l_1}}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-hardest-lepton-pT
XLabel=$p_{T,{l_2}}[\text{GeV}]$
XMax=200.0
RatioPlotXMax=200.0
 END PLOT


 BEGIN PLOT /WHIZARD_.*/W_plus-pT
XLabel=$p_{T,W^+}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-pT
XLabel=$p_{T,j_b j_b}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
XMax=350.0
RatioPlotXMax=350.0
LegendXPos=0.8
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-pT
XLabel=$p_{T,{BW^-}}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
XMax=350.0
RatioPlotXMax=350.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-pT
XLabel=$p_{T,W^+j_b} [\text{GeV}]$
XMax=400.0
RatioPlotXMax=400.0
RatioPlotYMax=1.8
LegendXPos=0.15
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blm-pT
XLabel=$p_{T,{Bl^-}}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
XMax=350.0
RatioPlotXMax=350.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blp-pT
XLabel=$p_{T,l^+ j_b}[\text{GeV}]$
XMax=355.0
RatioPlotXMax=355.0
LegendXPos=0.8
Rebin=1
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wm-pT
XLabel=$p_{T,{W^-}}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wp-pT
XLabel=$p_{T,{W^+}}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/electron-Pt
XLabel=$p_{T,{e^-}}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
XMax=350.0
RatioPlotXMax=350.0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/muon-Pt
XLabel=$p_{T,{\mu^+}}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
XMax=350.0
RatioPlotXMax=350.0
 END PLOT


 BEGIN PLOT /WHIZARD_.*/lepton-lepton-Pt
XLabel=$p_{T,{ll}}[\text{GeV}]$
 END PLOT










#===========#
#  E plots  #
#===========#
 BEGIN PLOT /WHIZARD_.*/.*-E$
YLabel=$\frac{d\sigma}{dE}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/leading-jet-E
XLabel=$E_{j_1}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-E
XLabel=$E_{j_2}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-jet-E
XLabel=$E_{b}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/hardest-lepton-E
XLabel=$E_{l_1}[\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/2nd-hardest-lepton-E
XLabel=$E_{l_2}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-E
XLabel=$E_{BB}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blm-E
XLabel=$E_{Bl^-}[\text{GeV}]$
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
XLabel=$E_{BW^-}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-E
XLabel=$E_{BW^+}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blp-E
XLabel=$E_{Bl^+}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blm-E
XLabel=$E_{Bl^-}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wm-E
XLabel=$E_{W^-}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wp-E
XLabel=$E_{W^+}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/electron-E
XLabel=$E_{e^-}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/muon-E
XLabel=$E_{\mu^+}[\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/lepton-lepton-E
XLabel=$E_{ll}[\text{GeV}]$
 END PLOT



 BEGIN PLOT /WHIZARD_.*/Wm-inv
XLabel=$m_{W^-}[\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/Wm-inv-peak
XLabel=$m_{W^-}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wp-inv
XLabel=$m_{W^+}[\text{GeV}]$
 END PLOT


 BEGIN PLOT /WHIZARD_.*/Wp-inv-peak
XLabel=$m_{W^+}[\text{GeV}]$
 END PLOT




#===============#
#  angle plots  #
#===============#
 BEGIN PLOT /WHIZARD_.*-Theta
YLabel=$\frac{d\sigma}{d{\cos{\theta}}}$[fb]
LegendXPos=0.8
LegendYPos=0.9
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
XLabel=$\cos\theta_{j_2}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-Theta
XLabel=$\cos\theta_{BB}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-Theta
XLabel=$\cos\theta_{W^+ j_b}$
YLabel=$\frac{d\sigma}{d\cos\theta}[\text{fb}]$
LegendXPos=0.75
RatioPlotYMin=0.8
RatioPlotYMax=1.2
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-Theta
XLabel=$\cos\theta_{BW^-}$
YLabel=$\frac{d\sigma}{d\cos\theta}[\text{fb}]$
LegendXPos=0.1
RatioPlotYMin=0.8
RatioPlotYMax=1.2
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blm-Theta
XLabel=$\cos\theta_{l^-j_{\bar b}}$
YLabel=$\frac{d\sigma}{d\cos\theta}[\text{fb}]$
RatioPlotYMin=0.95
RatioPlotYMax=1.25
LegendXPos=0.2
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Blp-Theta
XLabel=$\cos\theta_{l^+j_b}$
YLabel=$\frac{d\sigma}{d\cos\theta}[\text{fb}]$
RatioPlotYMin=0.95
RatioPlotYMax=1.25
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


 BEGIN PLOT /WHIZARD_.*hardest-lepton-eta
XLabel=$\eta^{l_1}$
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

