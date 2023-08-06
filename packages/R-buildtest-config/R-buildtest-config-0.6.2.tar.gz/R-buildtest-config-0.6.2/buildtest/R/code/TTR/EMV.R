library(TTR)
data(ttrc)
emv <- EMV(ttrc[,c("High","Low")], ttrc[,"Volume"])
