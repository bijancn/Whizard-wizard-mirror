#===================#
#  generator label  #
#===================#
 BEGIN SPECIAL /WHIZARD_.*
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.1,0.1){\color{gray}\textsc{Whizard+Omega}+\textsc{OpenLoops}}
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
 BEGIN PLOT /WHIZARD_2015_NLO
Title=$\quad e^+e^-\to W^+b W^-\bar{b}$, $\quad N_\text{jets}\geq 2$
 END PLOT

 BEGIN PLOT /WHIZARD_2015_NLO_ttbarcuts
Title=$\quad e^+e^-\to W^+b W^-\bar{b}$, $\quad N_\text{jets}\geq 2$, $\quad\lvert m_{Wb}-m_t\rvert\leq 1 \text{GeV}$
 END PLOT

#========================#
#  invariant mass plots  #
#========================#
 BEGIN PLOT /WHIZARD_.*/.*-inv
YLabel=$\frac{d\sigma}{dm}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/jets-inv
XLabel=$m(p^{j_1}+p^{j_2})$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/WW-inv
XLabel=$m_{WW}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BW-inv
LogY=1
XLabel=$m_{BW}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/BB-inv
XLabel=$m_{b\bar{b}}[\text{GeV}]$
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

 BEGIN PLOT /WHIZARD_.*/jet-pT-log
YLabel=$\frac{d\sigma}{d\sum_i\log{p_{T,j_i}}}[\text{fb}/\text{GeV}]$
XLabel=$\sum_i\log{p_{T,j_i}}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/gluon-pT
LogY=1
XLabel=$p_{T,g}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-quark-pT
XLabel=$p_{T,b}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/leading-jet-pT
XLabel=$p_T^{j_1}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/second-leading-jet-pT
XLabel=$p_T^{j_2}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/W_plus-pT
XLabel=$p_{T,W^+}[\text{GeV}]$
YLabel=$\frac{d\sigma}{dp_T}[\text{fb}/\text{GeV}]$
 END PLOT

#===========#
#  E plots  #
#===========#
 BEGIN PLOT /WHIZARD_.*/.*-E
YLabel=$\frac{d\sigma}{dE}[\text{fb}/\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/b-quark-E
XLabel=$E_{b}[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/gluon-E
LogY=1
XLabel=$E_g[\text{GeV}]$
 END PLOT

 BEGIN PLOT /WHIZARD_.*/W_plus-E
XLabel=$E_{W^+}[\text{GeV}]$
 END PLOT

#===============#
#  other plots  #
#===============#
 BEGIN PLOT /WHIZARD_.*/jet-count
YLabel=$\frac{d\sigma}{dN_\text{jets}}[\text{fb}]$
XLabel=$N_\text{jets}$
 END PLOT

