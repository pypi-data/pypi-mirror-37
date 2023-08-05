library(checkmate)
# Is R's home directory readable?
testDirectory(R.home(), "r")
# Is R's home directory readable and writable?
testDirectory(R.home(), "rw")

