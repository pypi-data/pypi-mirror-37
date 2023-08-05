library(ff)
message('create the ff file outside getOption("fftempir"),
it will have default finalizer "close", so you need to delete it explicitely')
x <- ff(1:12, pattern="./ffexample")
delete(x)
rm(x)

