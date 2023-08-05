library(ape)
TR <- replicate(10, rcoal(sample(11:20, size = 1)), simplify = FALSE)
kronoviz(TR)
kronoviz(TR, horiz = FALSE, type = "c", show.tip.label = FALSE)
