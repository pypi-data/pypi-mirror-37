library(ape)
q1 <- matrix(runif(36), nrow = 6)
q2 <- matrix(runif(36), nrow = 6)
mantel.test(q1, q2, graph = TRUE,
main = "Mantel test: a random example with 6 X 6 matrices",
xlab = "z-statistic", ylab = "Density",
sub = "The vertical line shows the observed z-statistic")

