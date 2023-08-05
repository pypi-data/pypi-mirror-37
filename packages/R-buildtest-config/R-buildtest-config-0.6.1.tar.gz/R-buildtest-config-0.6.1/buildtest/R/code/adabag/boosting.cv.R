library(adabag)
## rpart library should be loaded
data(iris)
iris.boostcv <- boosting.cv(Species ~ ., v=2, data=iris, mfinal=10,
control=rpart.control(cp=0.01))
iris.boostcv[-1]
## rpart and mlbench libraries should be loaded
## Data Vehicle (four classes)
#This example has been hidden to fulfill execution time <5s
#data(Vehicle)
#Vehicle.boost.cv <- boosting.cv(Class ~.,data=Vehicle,v=5, mfinal=10, coeflearn="Zhu",
#control=rpart.control(maxdepth=5))
#Vehicle.boost.cv[-1]

