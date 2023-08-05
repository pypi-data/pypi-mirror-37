library(checkmate)
# Can we create a file in the tempdir?
testPathForOutput(file.path(tempdir(), "process.log"))

