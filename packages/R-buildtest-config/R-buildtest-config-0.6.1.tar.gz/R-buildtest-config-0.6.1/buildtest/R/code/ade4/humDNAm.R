library(ade4)
data(humDNAm)
dpcoahum <- dpcoa(data.frame(t(humDNAm$samples)),
sqrt(humDNAm$distances), scan = FALSE, nf = 2)
plot(dpcoahum)
