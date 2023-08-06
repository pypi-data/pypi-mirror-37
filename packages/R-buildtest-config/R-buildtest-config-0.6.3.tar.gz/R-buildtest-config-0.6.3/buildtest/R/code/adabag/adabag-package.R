library(adabag)
## rpart library should be loaded
data(iris)
iris.adaboost <- boosting(Species~., data=iris, boos=TRUE,
mfinal=6)
importanceplot(iris.adaboost)
sub <- c(sample(1:50, 35), sample(51:100, 35), sample(101:150, 35))
iris.bagging <- bagging(Species ~ ., data=iris[sub,], mfinal=10)
#Predicting with labeled data
iris.predbagging<-predict.bagging(iris.bagging, newdata=iris[-sub,])
iris.predbagging
#Predicting with unlabeled data
iris.predbagging<- predict.bagging(iris.bagging, newdata=iris[-sub,-5])
iris.predbagging
