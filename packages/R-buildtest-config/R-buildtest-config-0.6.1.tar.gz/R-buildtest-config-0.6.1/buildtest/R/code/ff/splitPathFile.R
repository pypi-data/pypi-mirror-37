library(ff)
pathfile <- c("", ".", "/.", "./", "./.", "/"
, "a", "a/", "/a", "a/a", "./a", "a/.", "c:/a/b/c", "c:/a/b/c/"
, "..", "../", "/..", "../..", "//", "\\\\a\\", "\\\\a/"
, "\\\\a/b", "\\\\a/b/", "~", "~/", "~/a", "~/a/")
splitted <- splitPathFile(pathfile)
restored <- unsplitPathFile(splitted)
stopifnot(all(gsub("\\\\","/",restored)==gsub("\\\\","/",pathfile)))
dirnam <- dirname(pathfile)
basnam <- basename(pathfile)
db <- file.path(dirnam,basnam)
ident = gsub("\\\\","/",db) == gsub("\\\\","/",pathfile)
sum(!ident)
do.call("data.frame", c(list(ident=ident, pathfile=pathfile
, dirnam=dirnam, basnam=basnam), splitted))
## Not run:
message("show the difference between tempfile and fftempfile")
do.call("data.frame", c(list(ident=ident, pathfile=pathfile, dirnam=dirnam, basnam=basnam)
, splitted, list(filename=tempPathFile(splitted), fftempfile=fftempfile(pathfile))))
message("for a single string splitPathFile is slower,
for vectors of strings it scales much better than dirname+basename")
system.time(for (i in 1:1000){
d <- dirname(pathfile)
b <- basename(pathfile)
})
system.time(for (i in 1:1000){
s <- splitPathFile(pathfile)
})
len <- c(1,10,100,1000)
timings <- matrix(0, 2, length(len), dimnames=list(c("dir.base.name", "splitPathFile"), len))
for (j in seq(along=len)){
l <- len[j]
r <- 10000 / l
x <- rep("\\\\a/b/", l)
timings[1,j] <- system.time(for (i in 1:r){
d <- dirname(x)
b <- basename(x)
})[3]
timings[2,j] <- system.time(for (i in 1:r){
s <- splitPathFile(x)
})[3]
}
timings
## End(Not run)
