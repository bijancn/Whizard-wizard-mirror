 Generator label
 BEGIN SPECIAL /WHIZARD_2015_SINGLEEMISSION
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.1,0.1){\color{gray}\textsc{Whizard+Omega/GoSam}}
\endpsclip
 END SPECIAL

# General settings
 BEGIN PLOT /WHIZARD_2015_NLO
#ErrorBars=0
#ErrorBands=0
LogY=0
RatioPlotYLabel=K-Factor
RatioPlotSameStyle=1
LegendXPos=0.55
 END PLOT

 BEGIN PLOT /WHIZARD_2015_NLO/q-pT
XLabel=$p_T$
Title=Affen
 END PLOT

 BEGIN HISTOGRAM /WHIZARD_2015_NLO/q-pT
ErrorBars=0
ErrorBands=0
 END HISTOGRAM

 BEGIN HISTOGRAM /WHIZARD_2015_NLO/B-pT
ErrorBars=0
ErrorBands=0
 END HISTOGRAM

 BEGIN PLOT /WHIZARD_2015_NLO/B-pT
XLabel=$p_T^b[GeV]$
YLabel=$\frac{d\sigma}{dp_T^b}[fb/GeV]$
 END PLOT 

 BEGIN HISTOGRAM /WHIZARD_2015_NLO/W_plus-pT
ErrorBars=0
ErrorBands=0
 END HISTOGRAM

 BEGIN PLOT /WHIZARD_2015_NLO/W_plus-pT
XLabel=$p_T^W[GeV]$
YLabel=$\frac{d\sigma}{dp_T^W}[fb/GeV]$
 END PLOT 

 BEGIN PLOT /WHIZARD_2015_NLO/WW-inv
XLabel=$m_{WW}$
YLabel=$\frac{d\sigma}{dm_{WW}}[fb/GeV]$
 END PLOT 

 BEGIN HISTOGRAM /WHIZARD_2015_NLO/WW-inv
ErrorBars=0
ErrorBands=0
 END HISTOGRAM

 BEGIN HISTOGRAM /WHIZARD_2015_NLO/BB-inv
ErrorBars=0
ErrorBands=0
 END HISTOGRAM

 BEGIN PLOT /WHIZARD_2015_NLO/BB-inv
XLabel=$m_{b\bar{b}}$
YLabel=$\frac{d\sigma}{dm_{b\bar{b}}}[fb/GeV]$
 END PLOT

