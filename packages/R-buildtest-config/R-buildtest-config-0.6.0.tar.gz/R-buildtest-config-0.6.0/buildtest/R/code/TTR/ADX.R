library(TTR)
data(ttrc)
dmi.adx <- ADX(ttrc[,c("High","Low","Close")])
