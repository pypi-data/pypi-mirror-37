library(ade4)
data(rpjdl)
millog <- log(rpjdl$mil + 1)
iv1 <- cca(rpjdl$fau, millog, scan = FALSE)
randtest(iv1)

