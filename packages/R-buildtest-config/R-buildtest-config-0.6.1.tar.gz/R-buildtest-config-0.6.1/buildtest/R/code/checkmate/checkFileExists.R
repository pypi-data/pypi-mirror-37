library(checkmate)
# Check if R's COPYING file is readable
testFileExists(file.path(R.home(), "COPYING"), access = "r")
# Check if R's COPYING file is readable and writable
testFileExists(file.path(R.home(), "COPYING"), access = "rw")

