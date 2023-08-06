library(ade4)
data(aviurba)
for (i in 1:10) {
d <- dist.binary(aviurba$fau, method = i)
cat(attr(d, "method"), is.euclid(d), "\n")}

