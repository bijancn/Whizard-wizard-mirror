 BEGIN PLOT /WHIZARD_2015_SINGLEEMISSION/Thrust
XLabel=1-T

RatioPlotYLabel=Ratio
RatioPlotSameStyle=1
LegendXPos=0.55
#YLabel=$\frac{1}{\sigma$}{d\sigma}{dT}
# + any additional plot settings you might like, see make-plots documentation
 END PLOT

 BEGIN SPECIAL /WHIZARD_2015_SINGLEEMISSION/Thrust
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.1,0.1){\color{gray}\textsc{Whizard+Omega/GoSam}}
\endpsclip
 END SPECIAL

 BEGIN PLOT /WHIZARD_2015_SINGLEEMISSION/ThrustMajor
XLabel= Major

RatioPlotYLabel=Ratio
RatioPlotSameStyle=1
LegendXPos=0.55
 END PLOT

 BEGIN SPECIAL /WHIZARD_2015_SINGLEEMISSION/ThrustMajor
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.1,0.1){\color{gray}\textsc{Whizard+Omega/GoSam}}
\endpsclip
 END SPECIAL

 BEGIN PLOT /WHIZARD_2015_SINGLEEMISSION/ThrustMinor
XLabel=Minor

RatioPlotYLabel=Ratio
RatioPlotSameStyle=1
LegendXPos=0.55
 END PLOT

 BEGIN SPECIAL /WHIZARD_2015_SINGLEEMISSION/ThrustMinor
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.1,0.1){\color{gray}\textsc{Whizard+Omega/GoSam}}
\endpsclip
 END SPECIAL

 BEGIN PLOT /WHIZARD_2015_SINGLEEMISSION/Oblateness
XLabel=Oblateness

RatioPlotYLabel=Ratio
RatioPlotSameStyle=1
LegendXPos=0.55
 END PLOT

 BEGIN SPECIAL /WHIZARD_2015_SINGLEEMISSION/Oblateness
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.1,0.1){\color{gray}\textsc{Whizard+Omega/GoSam}}
\endpsclip
 END SPECIAL
