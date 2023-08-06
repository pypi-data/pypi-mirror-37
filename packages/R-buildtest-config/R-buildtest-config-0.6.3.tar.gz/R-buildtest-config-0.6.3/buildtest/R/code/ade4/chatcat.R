library(ade4)
data(chatcat)
summary(chatcat$tab)
w <- acm.disjonctif(chatcat$tab) # Disjonctive table
names(w) <- c(paste("A", 1:5, sep = ""), paste("B", 1:5, sep = ""),
paste("C", 1:2, sep = ""))
w <- t(w*chatcat$num)
w <- data.frame(w)
w # BURT table

