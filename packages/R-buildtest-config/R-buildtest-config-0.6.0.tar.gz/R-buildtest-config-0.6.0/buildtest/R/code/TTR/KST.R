library(TTR)
data(ttrc)
kst <- KST(ttrc[,"Close"])
kst4MA <- KST(ttrc[,"Close"],
maType=list(list(SMA),list(EMA),list(DEMA),list(WMA)))

