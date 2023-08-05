library(geepack)
data(ohio)
fit <- geese(resp ~ age + smoke + age:smoke, id=id, data=ohio,
family=binomial, corstr="exch", scale.fix=TRUE)
summary(fit)
fit.ar1 <- geese(resp ~ age + smoke + age:smoke, id=id, data=ohio,
family=binomial, corstr="ar1", scale.fix=TRUE)
summary(fit.ar1)
