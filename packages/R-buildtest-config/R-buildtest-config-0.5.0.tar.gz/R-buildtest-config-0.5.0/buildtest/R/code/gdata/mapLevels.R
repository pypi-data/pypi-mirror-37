library(gdata)
## --- Integer levelsMap ---
(f <- factor(sample(letters, size=20, replace=TRUE)))
(mapInt <- mapLevels(f))
## Integer to factor
(int <- as.integer(f))
(mapLevels(int) <- mapInt)
all.equal(int, f)
## Remap levels of a factor
(fac <- factor(as.integer(f)))
(mapLevels(fac) <- mapInt) # the same as levels(fac) <- mapInt
all.equal(fac, f)
## --- Character levelesMap ---
f1 <- factor(letters[1:10])
f2 <- factor(letters[5:14])
## Internal codes are the same, but levels are not
as.integer(f1)
as.integer(f2)
## Get character levelsMaps and combine them
mapCha1 <- mapLevels(f1, codes=FALSE)
mapCha2 <- mapLevels(f2, codes=FALSE)
(mapCha <- c(mapCha1, mapCha2))
## Remap factors
mapLevels(f1) <- mapCha # the same as levels(f1) <- mapCha
mapLevels(f2) <- mapCha # the same as levels(f2) <- mapCha
## Internal codes are now "consistent" among factors
as.integer(f1)
as.integer(f2)
## Remap characters to get factors
f1 <- as.character(f1); f2 <- as.character(f2)
mapLevels(f1) <- mapCha
mapLevels(f2) <- mapCha
## Internal codes are now "consistent" among factors
as.integer(f1)
as.integer(f2)

