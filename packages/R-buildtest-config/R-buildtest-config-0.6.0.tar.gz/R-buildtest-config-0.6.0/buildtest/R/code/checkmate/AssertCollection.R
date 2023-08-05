library(checkmate)
x = "a"
coll = makeAssertCollection()
print(coll$isEmpty())
assertNumeric(x, add = coll)
coll$isEmpty()
coll$push("Custom error message")
coll$getMessages()
## Not run:
reportAssertions(coll)
## End(Not run)
