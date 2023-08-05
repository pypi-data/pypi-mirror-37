library(checkmate)
testChoice("x", letters)
# x is converted before the comparison if necessary
# note that this is subject to change in a future version
testChoice(factor("a"), "a")
testChoice(1, "1")
testChoice(1, as.integer(1))


