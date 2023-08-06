library(ape)
# get tree
data("hivtree.newick") # example tree in NH format
tree.hiv <- read.tree(text = hivtree.newick) # load tree
# run mcmc chain
mcmc.out <- mcmc.popsize(tree.hiv, nstep=100, thinning=1, burn.in=0,progress.bar=FALSE) # toy run
#mcmc.out <- mcmc.popsize(tree.hiv, nstep=10000, thinning=5, burn.in=500) # remove comments!!
# make list of population size versus time
popsize <- extract.popsize(mcmc.out)
# plot and compare with skyline plot
sk <- skyline(tree.hiv)
plot(sk, lwd=1, lty=3, show.years=TRUE, subst.rate=0.0023, present.year = 1997)
lines(popsize, show.years=TRUE, subst.rate=0.0023, present.year = 1997)

