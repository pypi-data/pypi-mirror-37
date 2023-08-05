library(ape)
### Some random data...
data(bird.orders)
x <- rnorm(23, m=100)
### Reconstruct ancestral quantitative characters:
reconstruct(x, bird.orders)
reconstruct(x, bird.orders, method = "GLS_OUS", alpha=NULL)
