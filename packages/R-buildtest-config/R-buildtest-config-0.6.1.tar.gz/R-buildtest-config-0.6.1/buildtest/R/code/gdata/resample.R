library(gdata)
## sample behavior differs if first argument is scalar vs vector
sample( c(10) )
sample( c(10,10) )
## resample has the consistent behavior for both cases
resample( c(10) )
resample( c(10,10) )
