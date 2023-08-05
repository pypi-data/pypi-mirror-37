library(TTR)
data(ttrc)
trix <- TRIX(ttrc[,"Close"])
trix4 <- TRIX(ttrc[,"Close"],
maType=list(list(SMA), list(EMA, wilder=TRUE), list(SMA), list(DEMA)))
