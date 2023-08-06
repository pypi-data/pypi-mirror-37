library(ade4)
data(banque)
banque.acm <- dudi.acm(banque, scann = FALSE, nf = 3)
score(banque.acm, which = which(banque.acm$cr[, 1] > 0.2))
