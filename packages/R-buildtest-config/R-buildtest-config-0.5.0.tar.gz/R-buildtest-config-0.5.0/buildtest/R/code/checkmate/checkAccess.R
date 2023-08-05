library(checkmate)
# Is R's home directory readable?
testAccess(R.home(), "r")
# Is R's home directory writeable?
testAccess(R.home(), "w")

