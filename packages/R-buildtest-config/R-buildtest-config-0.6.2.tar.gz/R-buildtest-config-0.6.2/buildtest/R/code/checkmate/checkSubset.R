library(checkmate)
testSubset(c("a", "z"), letters)
testSubset("ab", letters)
testSubset("Species", names(iris))
# x is converted before the comparison if necessary
# note that this is subject to change in a future version
testSubset(factor("a"), "a")
testSubset(1, "1")
testSubset(1, as.integer(1))
