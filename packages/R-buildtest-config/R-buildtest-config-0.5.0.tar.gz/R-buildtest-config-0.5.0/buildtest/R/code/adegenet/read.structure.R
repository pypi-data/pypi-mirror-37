library(adegenet)
obj <- read.structure(system.file("files/nancycats.str",package="adegenet"),
onerowperind=FALSE, n.ind=237, n.loc=9, col.lab=1, col.pop=2, ask=FALSE)
obj

