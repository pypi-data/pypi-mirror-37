library(TTR)
data(ttrc)
vhf.close <- VHF(ttrc[,"Close"])
vhf.hilow <- VHF(ttrc[,c("High","Low","Close")])
