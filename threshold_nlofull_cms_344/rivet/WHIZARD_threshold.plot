#===================#
#  generator label  #
#===================#
 BEGIN SPECIAL /WHIZARD_.*
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.1,0.1){\color{gray}\textsc{Whizard}}
\endpsclip
 END SPECIAL

#====================#
#  general settings  #
#====================#
 BEGIN PLOT /WHIZARD_.*
LogY=1
RatioPlotYLabel=Scale vars
RatioPlotSameStyle=1
LegendXPos=0.75
YLabel=$\frac{d\sigma}{d\mathcal{O}}[\text{fb}/[a.u.]]$
RatioPlotYMax=1.2
RatioPlotYMin=0.8
 END PLOT

 BEGIN HISTOGRAM /WHIZARD_.*
ErrorBars=0
ErrorBands=0
 END HISTOGRAM

 BEGIN PLOT /WHIZARD_.*/.*A_FB.*
YLabel=$A_{FB}$
LogY=0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/.*Sum_Weights.*
YLabel=SumOfWeights
LogY=0
 END PLOT

#==========#
#  titles  #
#==========#
 BEGIN PLOT /WHIZARD_2W2b_NLO
Title=$\quad e^+e^-\to W^+b W^-\bar{b}$, $N_\text{jets}\geq 2, \quad \quad \sqrt{s} = 344 \text{GeV}$
 END PLOT

###################
#  global shapes  #
###################

 BEGIN PLOT /WHIZARD_.*/Aplanarity
XMax=0.3
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Planarity
XMax=0.5
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Thrust
XMax=0.45
XLabel=$1-T$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/ThrustMajor
XMax=0.75
XMin=0.05
XLabel=$T_{\text{major}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/ThrustMinor
XMax=0.50
XMin=0.0
XLabel=$T_{\text{minor}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Oblateness
XMax=0.7
XLabel=$O$
 END PLOT

#========================#
#  invariant mass plots  #
#========================#
 BEGIN PLOT /WHIZARD_.*/.*-inv
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jets-inv*
XLabel=$m^{jj}[\text{GeV}]$
XLabel=$m(p^{j_1}+p^{j_2})$
LogY=0
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jets-inv
XLabel=$m^{jj}[\text{GeV}]$
XMax=170
XMin=20
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jets-inv-Hpeak
XLabel=$m^{jj}[\text{GeV}]$
XMax=135
XMin=115
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jets-inv-Zpeak
XLabel=$m^{jj}[\text{GeV}]$
XMax=100
XMin=80
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BW-inv
XLabel=$m^{j_{b}W}[\text{GeV}]$
XMax=260
XMin=100
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BW-inv-peak
XLabel=$m^{j_{b}W}[\text{GeV}]$
XMax=180
XMin=160
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-inv
XLabel=$m^{j_{b}j_{\bar{b}}}[\text{GeV}]$
XMax=170
XMin=10
LegendXPos=0.60
LegendYPos=0.50
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-inv-Hpeak
XLabel=$m^{j_{b}j_{\bar{b}}}[\text{GeV}]$
XMax=135
XMin=115
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-inv-Zpeak
XLabel=$m^{j_{b}j_{\bar{b}}}[\text{GeV}]$
XMax=100
XMin=80
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-inv
XLabel=$m_{W^-j_b}[\text{GeV}]$
XMax=260
XMin=80
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-inv-peak
XLabel=$m^{W^-j_b}[\text{GeV}]$
XMax=180
XMin=160
LegendXPos=0.10
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-inv
XLabel=$m^{W^+j_{\bar b}}[\text{GeV}]$
XMax=260
XMin=80
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-inv-peak
XLabel=$m^{W^+j_{\bar b}}[\text{GeV}]$
XMax=180
XMin=160
 END PLOT

####################
#  threeMom plots  #
####################
 BEGIN PLOT /WHIZARD_.*/.*-ThreeMom
YLabel=$\frac{d\sigma}{d|\mathbf{p}|}[\text{fb}/\text{GeV}]$
XLabel=${|\mathbf{p}|}^{\bar{b}W^-}[\text{GeV}]$
XMax=90
XMin=10
RatioPlotYMax=1.3
RatioPlotYMin=0.7
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-ThreeMom
XLabel=${|\mathbf{p}|}^{W^- j_{\bar{b}}}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-ThreeMom
XLabel=${|\mathbf{p}|}^{W^+ j_{b}}[\text{GeV}]$
 END PLOT

#============#
#  pT plots  #
#============#
 BEGIN PLOT /WHIZARD_.*/.*-pT
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/leading-jet-pT
XLabel=$p_T^{j_1}[\text{GeV}]$
XMax=150
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-pT
XLabel=$p_T^{j_2}[\text{GeV}]$
XMax=85
LegendXPos=0.60
LegendYPos=0.50
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-jet-pT
XLabel=$p_T^{j_b}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/bbar-jet-pT
XLabel=$p_T^{j_{\bar{b}}}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wp-pT
XLabel=$p_T^{W^+}[\text{GeV}]$
XMax=150
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wm-pT
XLabel=$p_T^{W^-}[\text{GeV}]$
XMax=150
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-pT
XLabel=$p_T^{j_b j_{\bar b}}[\text{GeV}]$
XMax=270
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-pT
XLabel=$p_T^{W^- j_{\bar{b}}}[\text{GeV}]$
XMax=90
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-pT
XLabel=$p_T^{W^+ j_b}[\text{GeV}]$
XMax=90
 END PLOT


#===========#
#  E plots  #
#===========#
 BEGIN PLOT /WHIZARD_.*/.*-E
YLabel=$\frac{d\sigma}{dE}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/leading-jet-E
XLabel=$E^{j_1}[\text{GeV}]$
XMax=150
XMin=20
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-E
XLabel=$E^{j_2}[\text{GeV}]$
XMax=85
LegendXPos=0.10
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-jet-E
XLabel=$E^{b}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/bbar-jet-E
XLabel=$E^{\bar{b}}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wp-E
XLabel=$E^{W^+}[\text{GeV}]$
XMax=160
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wm-E
XLabel=$E^{W^-}[\text{GeV}]$
XMax=160
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-E
XLabel=$E^{j_bj_{\bar{b}}}[\text{GeV}]$
XMin=30
XMax=290
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-E
XLabel=$E^{W^- j_b}[\text{GeV}]$
XMax=260
XMin=100
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-E
XLabel=$E^{W^+ j_{\bar{b}}}[\text{GeV}]$
XMax=260
XMin=100
 END PLOT

#=========================#
#  angular distributions  #
#=========================#

 BEGIN PLOT /WHIZARD_.*/.*-Theta
YLabel=$\frac{d\sigma}{d\cos\theta}[\text{fb}]$
LogY=0
LegendXPos=0.60
LegendYPos=0.50
 END PLOT

 BEGIN PLOT /WHIZARD_.*/leading-jet-Theta
XLabel=$\cos\theta^{j_1}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/2nd-leading-jet-Theta
XLabel=$\cos\theta^{j_2}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-Theta
XLabel=$\cos\theta^{j_b j_{\bar{b}}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm-Theta
XLabel=$\cos\theta^{W^- j_{\bar{b}}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWp-Theta
XLabel=$\cos\theta^{W^+ j_b}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wm-Theta
XLabel=$\cos\theta^{W^-}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Wp-Theta
XLabel=$\cos\theta^{W^+}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-jet-Theta
XLabel=$\cos\theta^{j_b}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/bbar-jet-Theta
XLabel=$\cos\theta^{j_{\bar{b}}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-jet-Theta
XLabel=$\cos\theta^{j_b}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Phi.*
YLabel=$\frac{d\sigma}{d\Delta\phi}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Phi\(b\,Wm\)
XLabel=$\Delta\phi^{W^- j_{\bar{b}}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Phi\(b\,Wp\)
XLabel=$\phi^{W^+ j_b}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Phi\(b\,b\)
XLabel=$\phi^{j_b j_{\bar{b}}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/Phi\(b\,Wm\)
XLabel=$\phi^{W^- j_{\bar{b}}}$
 END PLOT

#==================#
#  rapidity plots  #
#==================#
 BEGIN PLOT /WHIZARD_.*/R\(b\,Wm\)
YLabel=$\frac{d\sigma}{dR}[\text{fb}/\text{GeV}]$
XLabel=$R^{W^- j_{\bar{b}}}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/R\(b\,Wp\)
YLabel=$\frac{d\sigma}{dR}[\text{fb}/\text{GeV}]$
XLabel=$R^{W^+ j_b}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/R\(b\,b\)
YLabel=$\frac{d\sigma}{dR}[\text{fb}/\text{GeV}]$
XLabel=$R^{j_b j_{\bar{b}}}$
 END PLOT

#===============#
#  other plots  #
#===============#

 BEGIN PLOT /WHIZARD_.*/jet-count
YLabel=$\frac{d\sigma}{dN_\text{jets}}[\text{fb}]$
XLabel=$N_\text{jets}$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BWm_BWp_invMass_peak
XLabel=$m^{BW^-}[\text{GeV}]$
YLabel=$m^{BW^+}[\text{GeV}]$
LogZ=0
 END PLOT
