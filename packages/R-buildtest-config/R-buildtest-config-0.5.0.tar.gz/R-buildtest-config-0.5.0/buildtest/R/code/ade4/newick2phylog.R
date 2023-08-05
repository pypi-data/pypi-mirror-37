library(ade4)
w <- "((((,,),,(,)),),(,));"
w.phy <- newick2phylog(w)
print(w.phy)
plot(w.phy)
## Not run:
# newick2phylog
data(newick.eg)
radial.phylog(newick2phylog(newick.eg[[8]], FALSE), cnode = 1,
clabel.l = 0.8)
w <- NULL
w[1] <- "(,((((((((((((((((,,(,(,))),),(((,(,)),(,)),),(,(,)),(,)),((((("
w[2] <- ",(,)),),),(,)),((((,((,),((,(,)),))),(,)),(,(,),,((,),(,)),)),("
w[3] <- "(((((,),),(,(,))),),(,)),(((,),),)))),((,,((,),)),(,)),((,),(,)"
w[4] <- ")),(((((((((,,),),,),),((,),)),(,),((,),)),),(((((,),),),((,),)"
w[5] <- "),(((,(,(,(,)))),(,)),(((,),(((((((,),),),,),(,)),(,)),)),((,)"
w[6] <- ",))))),(,((,),(,)),((,(,)),)))),((((,(,(,))),((,(,)),,((,(,)),)"
w[7] <- ",)),(((,),),(((,),),))),((,),))),((((((((((,,,,(,)),),((,),)),("
w[8] <- ",(,))),(((((((((,(,)),(,)),((((,((,),(,(,(,))))),((,),(,(,)))),"
w[9] <- "),((,),))),(((((((((,(,)),((,),(,))),),),),(((,((,),)),),((,((,"
w[10] <- "),)),)),(,)),(,(,(,)))),((((,(,)),(,)),(((,),(,)),(,),,(,))),(,"
w[11] <- "))),(,,,))),((((,),),),(((,(,(,))),((,),)),(,)))),(,)),),(,((,("
w[12] <- ",)),),(((,),),))),),(((,),),(,),(,(,))),(((,),(,)),((,),(,)))),"
w[13] <- "(((,),((,),)),(((((,,,,,),(,)),(,)),(,((,),))),))),(,(((((,(((("
w[14] <- ",(,)),),),)),),((,((,),((,((,),(,))),))),)),((((,),(((,),(,(,))"
w[15] <- "),)),),)),((,),)))),(((,((,,((,),)),)),),((,),))),((,),(,))),(("
w[16] <- ",),)),(((((,),((,(,)),(((,(,)),(,(((,),),))),))),(,),,),),),,(,"
w[17] <- ")),((((,),,),),((,,,),((,),((,),))))),((((((,(,)),,(,)),,(,),(,"
w[18] <- "),),(((((,(,(,),)),(((,),,),(,))),),),),,,((,),)),),)),(((((,),"
w[19] <- "(,(,)),),((,((,),),,),)),(((((((,),((((,,,),(,(,))),(((,(,)),),"
w[20] <- "(,))),)),),),),(,)),),),((,),))),((,),)),(((((((((((,),),(((((("
w[21] <- ",),),((,),)),(,)),),)),(,)),),((((((,),),(((,),),)),(,)),),(,))"
w[22] <- ",),),),),(,)),),((,),(,),,,)),(,(,(,)))),),(,)),),);"
phy1 <- newick2phylog(w,FALSE)
phy1
radial.phylog(phy1, clabel.l = 0, circle = 2.2, clea = 0.5,
cnod = 0.5)
data(newick.eg)
radial.phylog(newick2phylog(newick.eg[[8]], FALSE), cnode = 1,
clabel.l = 0.8)
# hclust2phylog
data(USArrests)
hc <- hclust(dist(USArrests), "ave")
par(mfrow = c(1,2))
plot(hc, hang = -1)
phy <- hclust2phylog(hc)
plot(phy, clabel.l = 0.75, clabel.n = 0.6, f = 0.75)
par(mfrow = c(1,1))
row.names(USArrests)
names(phy$leaves) #WARNING not the same for two reasons
row.names(USArrests) <- gsub(" ","_",row.names(USArrests))
row.names(USArrests)
names(phy$leaves) #WARNING not the same for one reason
USArrests <- USArrests[names(phy$leaves),]
row.names(USArrests)
names(phy$leaves) #the same
table.phylog(data.frame(scalewt(USArrests)), phy, csi = 2.5,
clabel.r = 0.75, f = 0.7)
#taxo2phylog
data(taxo.eg)
tax <- as.taxo(taxo.eg[[1]])
tax.phy <- taxo2phylog(as.taxo(taxo.eg[[1]]))
par(mfrow = c(1,2))
plot(tax.phy, clabel.l = 1.25, clabel.n = 1.25, f = 0.75)
plot(taxo2phylog(as.taxo(taxo.eg[[1]][sample(15),])),
clabel.l = 1.25, clabel.n = 1.25, f = 0.75)
par(mfrow=c(1,1))
plot(taxo2phylog(as.taxo(taxo.eg[[2]])), clabel.l = 1,
clabel.n = 0.75, f = 0.65)
## End(Not run)
