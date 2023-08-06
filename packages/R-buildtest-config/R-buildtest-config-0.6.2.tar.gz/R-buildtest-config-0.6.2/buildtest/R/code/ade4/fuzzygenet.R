library(ade4)
data(casitas)
casitas[1:5, ]
casitas <- fuzzygenet(casitas)
attributes(casitas)
rm(casitas)
