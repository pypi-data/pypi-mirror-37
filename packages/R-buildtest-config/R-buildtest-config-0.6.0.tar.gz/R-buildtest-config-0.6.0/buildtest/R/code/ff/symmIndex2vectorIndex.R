library(ff)
symmIndex2vectorIndex(rbind(
c(1,1)
,c(1,10)
,c(10,1)
,c(10,10)
), dim=c(10,10))
symmIndex2vectorIndex(rbind(
c(1,1)
,c(1,10)
,c(10,1)
,c(10,10)
), dim=c(10,10), fixdiag=1)
