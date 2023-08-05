library(TTR)
## Get Data and Indicator ##
data(ttrc)
zz <- ZigZag( ttrc[,c("High", "Low")], change=20 )
