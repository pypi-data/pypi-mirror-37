library(ade4)
data(worksurv)
acm1 <- dudi.acm(worksurv, row.w = attr(worksurv, "counts"), scan = FALSE)
if(adegraphicsLoaded()) {
s.class(acm1$li, worksurv)
} else {
par(mfrow = c(2, 2))
apply(worksurv, 2, function(x) s.class(acm1$li, factor(x), attr(worksurv, 'counts')))
par(mfrow = c(1, 1))
}
