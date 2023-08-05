library(ape)
## Simple example using data without correlations or phylogenetic
## signal. This illustrates the structure of the input data.
phy <- rcoal(10, tip.label = 1:10)
X <- matrix(rnorm(20), nrow = 10, ncol = 2)
rownames(X) <- phy$tip.label
U <- list(NULL, matrix(rnorm(10, mean = 10, sd = 4), nrow = 10, ncol = 1))
rownames(U[[2]]) <- phy$tip.label
SeM <- matrix(c(0.2, 0.4), nrow = 10, ncol = 2)
rownames(SeM) <- phy$tip.label
corphylo(X = X, SeM = SeM, U = U, phy = phy, method = "Nelder-Mead")
## Not run:
## Simulation example for the correlation between two variables. The
## example compares the estimates of the correlation coefficients from
## corphylo when measurement error is incorporated into the analyses with
## three other cases: (i) when measurement error is excluded, (ii) when
## phylogenetic signal is ignored (assuming a "star" phylogeny), and (iii)
## neither measurement error nor phylogenetic signal are included.
## In the simulations, variable 2 is associated with a single
## independent variable. This requires setting up a list U that has 2
## elements: element U[[1]] is NULL and element U[[2]] is a n x 1 vector
## containing simulated values of the independent variable.
# Set up parameter values for simulating data
n <- 50
phy <- rcoal(n, tip.label = 1:n)
R <- matrix(c(1, 0.7, 0.7, 1), nrow = 2, ncol = 2)
d <- c(0.3, .95)
B2 <- 1
Se <- c(0.2, 1)
SeM <- matrix(Se, nrow = n, ncol = 2, byrow = T)
rownames(SeM) <- phy$tip.label
# Set up needed matrices for the simulations
p <- length(d)
star <- stree(n)
star$edge.length <- array(1, dim = c(n, 1))
star$tip.label <- phy$tip.label
Vphy <- vcv(phy)
Vphy <- Vphy/max(Vphy)
Vphy <- Vphy/exp(determinant(Vphy)$modulus[1]/n)
tau <- matrix(1, nrow = n, ncol = 1)
C <- matrix(0, nrow = p * n, ncol = p * n)
for (i in 1:p) for (j in 1:p) {
Cd <- (d[i]^tau * (d[j]^t(tau)) * (1 - (d[i] * d[j])^Vphy))/(1 - d[i] * d[j])
C[(n * (i - 1) + 1):(i * n), (n * (j - 1) + 1):(j * n)] <- R[i, j] * Cd
}
MM <- matrix(SeM^2, ncol = 1)
V <- C + diag(as.numeric(MM))
## Perform a Cholesky decomposition of Vphy. This is used to generate
## phylogenetic signal: a vector of independent normal random variables,
## when multiplied by the transpose of the Cholesky deposition of Vphy will
## have covariance matrix equal to Vphy.
iD <- t(chol(V))
# Perform Nrep simulations and collect the results
Nrep <- 100
cor.list <- matrix(0, nrow = Nrep, ncol = 1)
cor.noM.list <- matrix(0, nrow = Nrep, ncol = 1)
cor.noP.list <- matrix(0, nrow = Nrep, ncol = 1)
cor.noMP.list <- matrix(0, nrow = Nrep, ncol = 1)
d.list <- matrix(0, nrow = Nrep, ncol = 2)
d.noM.list <- matrix(0, nrow = Nrep, ncol = 2)
B.list <- matrix(0, nrow = Nrep, ncol = 3)
B.noM.list <- matrix(0, nrow = Nrep, ncol = 3)
B.noP.list <- matrix(0, nrow = Nrep, ncol = 3)
for (rep in 1:Nrep) {
XX <- iD
X <- matrix(XX, nrow = n, ncol = 2)
rownames(X) <- phy$tip.label
U <- list(NULL, matrix(rnorm(n, mean = 2, sd = 10), nrow = n, ncol = 1))
rownames(U[[2]]) <- phy$tip.label
colnames(U[[2]]) <- "V1"
X[,2] <- X[,2] + B2[1] * U[[2]][,1] - B2[1] * mean(U[[2]][,1])
z <- corphylo(X = X, SeM = SeM, U = U, phy = phy, method = "Nelder-Mead")
z.noM <- corphylo(X = X, U = U, phy = phy, method = "Nelder-Mead")
z.noP <- corphylo(X = X, SeM = SeM, U = U, phy = star, method = "Nelder-Mead")
cor.list[rep] <- z$cor.matrix[1, 2]
cor.noM.list[rep] <- z.noM$cor.matrix[1, 2]
cor.noP.list[rep] <- z.noP$cor.matrix[1, 2]
cor.noMP.list[rep] <- cor(cbind(lm(X[,1] ~ 1)$residuals, lm(X[,2] ~ U[[2]])$residuals))[1,2]
d.list[rep, ] <- z$d
d.noM.list[rep, ] <- z.noM$d
B.list[rep, ] <- z$B
B.noM.list[rep, ] <- z.noM$B
B.noP.list[rep, ] <- z.noP$B
show(c(rep, z$convcode, z$cor.matrix[1, 2], z$d))
}
correlation <- rbind(R[1, 2], mean(cor.list), mean(cor.noM.list),
mean(cor.noP.list), mean(cor.noMP.list))
rownames(correlation) <- c("True", "With SeM and Phy", "Without SeM",
"Without Phy", "Without Phy or SeM")
correlation
signal.d <- rbind(d, colMeans(d.list), colMeans(d.noM.list))
rownames(signal.d) <- c("True", "With SeM and Phy", "Without SeM")
signal.d
est.B <- rbind(c(0, 0, B2), colMeans(B.list), colMeans(B.noM.list),
colMeans(B.noP.list))
rownames(est.B) <- c("True", "With SeM and Phy", "Without SeM", "Without Phy")
colnames(est.B) <- rownames(z$B)
est.B
# Example simulation output
# correlation
# [,1]
# True 0.7000000
# With SeM and Phy 0.7055958
# Without SeM 0.3125253
# Without Phy 0.4054043
# Without Phy or SeM 0.3476589
# signal.d
# [,1] [,2]
# True 0.300000 0.9500000
# With SeM and Phy 0.301513 0.9276663
# Without SeM 0.241319 0.4872675
# est.B
# B1.0 B2.0 B2.V1
# True 0.00000000 0.0000000 1.0000000
# With SeM and Phy -0.01285834 0.2807215 0.9963163
# Without SeM 0.01406953 0.3059110 0.9977796
# Without Phy 0.02139281 0.3165731 0.9942140
## End(Not run)

