 Generator label
 BEGIN SPECIAL /WHIZARD_2W2b_NLO
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.1,0.1){\color{gray}\textsc{Whizard+Omega/OpenLoops}}
\endpsclip
 END SPECIAL

# General settings
 BEGIN PLOT /WHIZARD_2W2b_NLO
LogY=0
RatioPlotYLabel=K-Factor
RatioPlotSameStyle=1
LegendXPos=0.55
YLabel=$\frac{d\sigma}{d\mathcal{O}}[fb/[a.u.]]$
 END PLOT

 BEGIN HISTOGRAM /WHIZARD_2W2b_NLO
ErrorBars=1
ErrorBands=0
 END HISTOGRAM

 BEGIN PLOT /WHIZARD_2W2b_NLO/jets-inv
XLabel=$m(p^{j_1}+p^{j_2})$
 END PLOT

 BEGIN PLOT /WHIZARD_2W2b_NLO/jet-pT
XLabel=$\sum_i p_T^{j_i}[GeV]$
 END PLOT

 BEGIN PLOT /WHIZARD_2W2b_NLO/jet-pT-log
XLabel=$\log{\sum_i p_T^{j_i}[GeV]}$
 END PLOT

 BEGIN PLOT /WHIZARD_2W2b_NLO/B-pT
XLabel=$p_T^b[GeV]$
YLabel=$\frac{d\sigma}{dp_T^b}[fb/GeV]$
 END PLOT

 BEGIN PLOT /WHIZARD_2W2b_NLO/leading-jet-pT
XLabel=$p_T^{j_1}[GeV]$
 END PLOT

 BEGIN PLOT /WHIZARD_2W2b_NLO/second-leading-jet-pT
XLabel=$p_T^{j_2}[GeV]$
 END PLOT

 BEGIN PLOT /WHIZARD_2W2b_NLO/W_plus-pT
XLabel=$p_T^W[GeV]$
YLabel=$\frac{d\sigma}{dp_T^W}[fb/GeV]$
 END PLOT

 BEGIN PLOT /WHIZARD_2W2b_NLO/WW-inv
XLabel=$m_{WW}$
YLabel=$\frac{d\sigma}{dm_{WW}}[fb/GeV]$
 END PLOT

 BEGIN PLOT /WHIZARD_2W2b_NLO/BB-inv
XLabel=$m_{b\bar{b}}$
YLabel=$\frac{d\sigma}{dm_{b\bar{b}}}[fb/GeV]$
 END PLOT
