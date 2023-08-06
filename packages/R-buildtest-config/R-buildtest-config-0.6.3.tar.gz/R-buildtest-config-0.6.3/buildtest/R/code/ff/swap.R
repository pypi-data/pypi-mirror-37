library(ff)
x <- ff("a", levels=letters, length=52)
y <- swap(x, "b", sample(length(x), 26))
x
y
rm(x,y); gc()

