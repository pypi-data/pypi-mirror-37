library(ade4)
data(morphosport)
plot(discrimin(dudi.pca(morphosport$tab, scan = FALSE),
morphosport$sport, scan = FALSE))
