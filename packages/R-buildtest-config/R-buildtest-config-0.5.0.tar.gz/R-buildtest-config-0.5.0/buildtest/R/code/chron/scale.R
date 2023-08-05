library(chron)
if(require("ggplot2")) {
dd <- data.frame(tt = chron(1:10), value = 101:110)
p <- ggplot(dd, aes(tt, value)) +
geom_point() + scale_x_chron(format = "%m-%d")
print(p)
}
