library(checkmate)
testList(list())
testList(as.list(iris), types = c("numeric", "factor"))
