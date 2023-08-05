library(TTR)
## Get Data and Indicator ##
data(ttrc)
trend <- aroon( ttrc[,c("High", "Low")], n=20 )

