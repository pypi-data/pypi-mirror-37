library(TTR)
data(ttrc)
roc <- ROC(ttrc[,"Close"])
mom <- momentum(ttrc[,"Close"])
