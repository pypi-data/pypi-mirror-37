library(gdata)
data(iris)
iris[duplicated(iris), ] # 2nd duplicated value
iris[duplicated(iris, fromLast=TRUE), ] # 1st duplicated value
iris[duplicated2(iris), ] # both duplicated values

