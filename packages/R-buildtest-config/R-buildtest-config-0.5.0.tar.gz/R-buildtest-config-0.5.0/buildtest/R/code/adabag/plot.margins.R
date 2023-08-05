library(adabag)
data(BreastCancer)
l <- length(BreastCancer[,1])
sub <- sample(1:l,2*l/3)
cntrl <- rpart.control(maxdepth = 3, minsplit = 0, cp = -1)
BC.adaboost <- boosting(Class ~.,data=BreastCancer[sub,-1],mfinal=15, control=cntrl)
BC.adaboost.pred <- predict.boosting(BC.adaboost,newdata=BreastCancer[-sub,-1])
BC.margins<-margins(BC.adaboost,BreastCancer[sub,-1]) # training set
BC.predmargins<-margins(BC.adaboost.pred,BreastCancer[-sub,-1]) # test set
plot.margins(BC.predmargins,BC.margins)

