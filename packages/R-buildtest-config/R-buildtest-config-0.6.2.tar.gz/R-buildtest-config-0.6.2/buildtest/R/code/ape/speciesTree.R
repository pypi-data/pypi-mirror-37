library(ape)
### example in Liu et al. (2010):
tr1 <- read.tree(text = "(((B:0.05,C:0.05):0.01,D:0.06):0.04,A:0.1);")
tr2 <- read.tree(text = "(((A:0.07,C:0.07):0.02,D:0.09):0.03,B:0.12);")
TR <- c(tr1, tr2)
TSmax <- speciesTree(TR) # MAXTREE
TSsha <- speciesTree(TR, mean) # shallowest divergence
layout(matrix(1:4, 1))
## playing with 'x.lim' is not so complicated
## but this will be improved someday
plot(tr1, "c", d = "u", y.lim = c(-0.07, 0.1), font = 1)
axisPhylo(4); title("Gene tree 1")
plot(tr2, "c", d = "u", y.lim = c(-0.05, 0.12), font = 1)
axisPhylo(4); title("Gene tree 2")
plot(TSmax, "c", d = "u", y.lim = c(-0.1, 0.07), font = 1)
axisPhylo(4); title("Species tree inferred\nby MAXTREE")
plot(TSsha, "c", d = "u", y.lim = c(0, 0.17), font = 1)
axisPhylo(4); title("Species tree inferred\nby Shallowest Divergence")

