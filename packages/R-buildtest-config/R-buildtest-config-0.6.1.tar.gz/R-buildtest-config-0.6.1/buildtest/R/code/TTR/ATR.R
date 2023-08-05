library(TTR)
data(ttrc)
atr <- ATR(ttrc[,c("High","Low","Close")], n=14)
