library(assertthat)
x <- 1
# assert_that() generates errors, so can't be usefully run in
# examples
## Not run:
assert_that(is.character(x))
assert_that(length(x) == 3)
assert_that(is.dir("asdf"))
y <- tempfile()
writeLines("", y)
assert_that(is.dir(y))
assert_that(FALSE, msg = "Custom error message")
## End(Not run)
# But see_if just returns the values, so you'll see that a lot
# in the examples: but remember to use assert_that in your code.
see_if(is.character(x))
see_if(length(x) == 3)
see_if(is.dir(17))
see_if(is.dir("asdf"))
see_if(5 < 3, msg = "Five is not smaller than three")
