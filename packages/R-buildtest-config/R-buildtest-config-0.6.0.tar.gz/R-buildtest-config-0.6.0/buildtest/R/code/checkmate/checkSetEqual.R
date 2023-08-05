library(checkmate)
testSetEqual(c("a", "b"), c("a", "b"))
testSetEqual(1:3, 1:4)
# x is converted before the comparison if necessary
# note that this is subject to change in a future version
testSetEqual(factor("a"), "a")
testSetEqual(1, "1")
testSetEqual(1, as.integer(1))

