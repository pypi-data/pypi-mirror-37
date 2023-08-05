library(checkmate)
# Create an object with classes "foo" and "bar"
x = 1
class(x) = c("foo", "bar")
# is x of class "foo"?
testClass(x, "foo")
# is x of class "foo" and "bar"?
testClass(x, c("foo", "bar"))
# is x of class "foo" or "bar"?
## Not run:
assert(
checkClass(x, "foo"),
checkClass(x, "bar")
)
## End(Not run)
# is x most specialized as "bar"?
testClass(x, "bar", ordered = TRUE)
