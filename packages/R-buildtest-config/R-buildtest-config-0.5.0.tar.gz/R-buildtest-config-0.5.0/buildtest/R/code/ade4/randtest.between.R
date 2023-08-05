library(ade4)
data(meaudret)
pca1 <- dudi.pca(meaudret$env, scan = FALSE, nf = 3)
rand1 <- randtest(bca(pca1, meaudret$design$season, scan = FALSE), 99)
rand1
plot(rand1, main = "Monte-Carlo test")
