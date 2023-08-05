library(chron)
x <- chron(dates = c("02/27/92", "02/27/92", "01/14/92", "02/28/92"),
times = c("23:03:20", "22:29:56", "01:03:30", "18:21:03"))
h <- hours(x)
y <- runif(4)
boxplot(y ~ h)
