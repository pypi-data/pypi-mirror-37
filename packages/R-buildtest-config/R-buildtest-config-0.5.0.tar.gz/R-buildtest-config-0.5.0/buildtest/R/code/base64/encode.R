library(base64)
# encode a file
myfile <- R.home("COPYING")
tmp <- tempfile()
base64::encode(myfile, tmp)
# decode it back
orig <- tempfile()
base64::decode(tmp, orig)
readLines(orig)

