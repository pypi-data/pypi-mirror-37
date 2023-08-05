library(checkmate)
# Simple custom check function
checkFalse = function(x) if (!identical(x, FALSE)) "Must be FALSE" else TRUE
# Create the respective expect function
expect_false = function(x, info = NULL, label = vname(x)) {
res = checkFalse(x)
makeExpectation(x, res, info = info, label = label)
}
# Alternative: Automatically create such a function
expect_false = makeExpectationFunction(checkFalse)
print(expect_false)
