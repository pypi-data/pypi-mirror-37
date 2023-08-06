library(assertthat)
not_empty(numeric())
not_empty(mtcars[0, ])
not_empty(mtcars[, 0])
