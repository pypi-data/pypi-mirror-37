library(TTR)
data(ttrc)
cmf <- CMF(ttrc[,c("High","Low","Close")], ttrc[,"Volume"])
