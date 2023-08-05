library(ff)
## Not run:
message("Neither giving pattern nor filename gives a random filename
with extension ffextension in fftempdir")
x <- ff(1:12)
finalizer(x)
filename(x)
message("Giving a pattern with just a prefix moves to a random filename
beginning with the prefix in fftempdir")
pattern(x) <- "myprefix_"
filename(x)
message("Giving a pattern with a path and prefix moves to a random filename
beginning with prefix in path (use . for getwd) ")
pattern(x) <- "./myprefix"
filename(x)
message("Giving a filename moves to exactly this filename and extension
in the R-expected place) ")
if (!file.exists("./myfilename.myextension")){
filename(x) <- "./myfilename.myextension"
filename(x)
}
message("NOTE that the finalizer has changed from 'delete' to 'close':
now WE are responsible for deleting the file - NOT the finalizer")
finalizer(x)
delete(x)
rm(x)
## End(Not run)

