library(ade4)
## Not run:
data(microsatt)
fac <- factor(rep(microsatt$loci.names, microsatt$loci.eff))
w <- dudi.coa(data.frame(t(microsatt$tab)), scann = FALSE)
wit <- wca(w, fac, scann = FALSE)
microsatt.ktab <- ktab.within(wit)
plot(sepan(microsatt.ktab)) # 9 separated correspondence analyses
plot(mcoa(microsatt.ktab, scan = FALSE))
plot(mfa(microsatt.ktab, scan = FALSE))
plot(statis(microsatt.ktab, scan = FALSE))
## End(Not run)
