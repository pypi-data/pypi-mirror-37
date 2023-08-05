library(gdata)
## works for vectors..
v <- 1:10
first(v)
last(v)
## and for lists
l <- list(a=1, b=2, c=3)
first(l)
last(l)
## and data.frames
df <- data.frame(a=1:2, b=3:4, c=5:6)
first(df)
last(df)
## and matrixes
m <- as.matrix(df)
first(m)
last(m)
