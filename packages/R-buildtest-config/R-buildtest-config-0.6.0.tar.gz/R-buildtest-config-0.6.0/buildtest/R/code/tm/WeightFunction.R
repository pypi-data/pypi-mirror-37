library(tm)
weightCutBin <- WeightFunction(function(m, cutoff) m > cutoff,
"binary with cutoff", "bincut")
