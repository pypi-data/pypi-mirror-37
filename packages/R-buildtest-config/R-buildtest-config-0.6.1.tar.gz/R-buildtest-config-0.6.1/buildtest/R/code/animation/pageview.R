library(animation)
plot(pageview[, 1:2], type = "b", col = "red", main = "Number of Visits in Yihui's Web")
## partial auto-correlation
pacf(pageview$visits)
