library(ff)
x <- ff(letters, levels=letters)
y <- clone(x, length=52)
rm(x,y); gc()
