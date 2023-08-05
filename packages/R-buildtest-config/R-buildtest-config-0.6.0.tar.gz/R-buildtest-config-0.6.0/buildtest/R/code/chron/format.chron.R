library(chron)
format(chron(0, 0), c("yy/m/d", "h:m:s"), sep = "T", enclose = c("", ""))
format(chron(0, 0), "%Y-%m-%dT%H:%M:%S") # same

