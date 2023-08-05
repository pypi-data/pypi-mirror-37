library(cluster)
data(animals)
apply(animals,2, table) # simple overview
ma <- mona(animals)
ma
## Plot similar to Figure 10 in Struyf et al (1996)
plot(ma)

