library(testthat)
x <- c(a = 1, b = 2, c = 3)
expect_named(x)
expect_named(x, c("a", "b", "c"))
# Use options to control sensitivity
expect_named(x, c("B", "C", "A"), ignore.order = TRUE, ignore.case = TRUE)
# Can also check for the absence of names with NULL
z <- 1:4
expect_named(z, NULL)
