library(gdata)
object.size(letters)
object.size(ls)
## find the 10 largest objects in the base package
allObj <- sapply(ls("package:base"),
function(x)
object.size(get(x, envir = baseenv()))
)
( bigObj <- as.object_sizes(rev(sort(allObj))[1:10] ) )
print(bigObj, humanReadable=TRUE)
as.object_sizes(14567567)
options(humanReadable=TRUE)
(
z <- object.size(letters,
c(letters, letters),
rep(letters, 100),
rep(letters, 10000)
)
)
is.object_sizes(z)
as.object_sizes(14567567)

