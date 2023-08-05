library(TTR)
data(ttrc)
macd <- MACD( ttrc[,"Close"], 12, 26, 9, maType="EMA" )
macd2 <- MACD( ttrc[,"Close"], 12, 26, 9,
maType=list(list(SMA), list(EMA, wilder=TRUE), list(SMA)) )
