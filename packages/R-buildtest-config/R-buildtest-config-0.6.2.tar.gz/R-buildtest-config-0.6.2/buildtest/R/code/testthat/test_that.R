library(testthat)
test_that("trigonometric functions match identities", {
expect_equal(sin(pi / 4), 1 / sqrt(2))
expect_equal(cos(pi / 4), 1 / sqrt(2))
expect_equal(tan(pi / 4), 1)
})
# Failing test:
## Not run:
test_that("trigonometric functions match identities", {
expect_equal(sin(pi / 4), 1)
})
## End(Not run)

