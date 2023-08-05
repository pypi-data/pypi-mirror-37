library(checkmate)
ee = as.environment(list(a = 1))
testEnvironment(ee)
testEnvironment(ee, contains = "a")

