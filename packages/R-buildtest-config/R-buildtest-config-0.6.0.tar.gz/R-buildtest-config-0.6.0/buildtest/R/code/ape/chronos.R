library(ape)
tr <- rtree(10)
### the default is the correlated rate model:
chr <- chronos(tr)
### strict clock model:
ctrl <- chronos.control(nb.rate.cat = 1)
chr.clock <- chronos(tr, model = "discrete", control = ctrl)
### How different are the rates?
attr(chr, "rates")
attr(chr.clock, "rates")
## Not run:
cal <- makeChronosCalib(tr, interactive = TRUE)
cal
### if you made mistakes, you can edit the data frame with:
### fix(cal)
chr <- chronos(tr, calibration = cal)
## End(Not run)
