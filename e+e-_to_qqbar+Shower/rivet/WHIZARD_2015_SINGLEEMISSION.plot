# Generator label
 BEGIN SPECIAL /WHIZARD_2015_SINGLEEMISSION
\psclip{\psframe[linewidth=0,linestyle=none](0,0)(1,1)}
\rput[bl](0.1,0.1){\color{gray}\textsc{Whizard+Omega/GoSam}}
\endpsclip
 END SPECIAL

# General settings
 BEGIN PLOT /WHIZARD_2015_SINGLEEMISSION
RatioPlotYLabel=Ratio
RatioPlotSameStyle=1
LegendXPos=0.55
 END PLOT

 BEGIN PLOT /WHIZARD_2015_SINGLEEMISSION/Thrust
XLabel=1-T
 END PLOT

 BEGIN PLOT /WHIZARD_2015_SINGLEEMISSION/ThrustMajor
XLabel= Major
 END PLOT

 BEGIN PLOT /WHIZARD_2015_SINGLEEMISSION/ThrustMinor
XLabel=Minor
 END PLOT

 BEGIN PLOT /WHIZARD_2015_SINGLEEMISSION/Oblateness
XLabel=Oblateness
 END PLOT
