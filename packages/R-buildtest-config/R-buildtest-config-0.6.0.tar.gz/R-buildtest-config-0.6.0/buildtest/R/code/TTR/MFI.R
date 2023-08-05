library(TTR)
data(ttrc)
mfi <- MFI(ttrc[,c("High","Low","Close")], ttrc[,"Volume"])

