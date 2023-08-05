library(gdata)
f <- factor(c("A", "B", "C", "D"))[1:3]
drop.levels(f)
l <- list(f=f, i=1:3, c=c("A", "B", "D"))
drop.levels(l)
df <- as.data.frame(l)
str(df)
str(drop.levels(df))

