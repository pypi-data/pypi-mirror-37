library(testthat)
with_mock(
all.equal = function(x, y, ...) TRUE,
expect_equal(2 * 3, 4),
.env = "base"
)
with_mock(
`base::identical` = function(x, y, ...) TRUE,
`base::all.equal` = function(x, y, ...) TRUE,
expect_equal(x <- 3 * 3, 6),
expect_identical(x + 4, 9)
)
## Not run:
expect_equal(3, 5)
expect_identical(3, 5)
## End(Not run)
