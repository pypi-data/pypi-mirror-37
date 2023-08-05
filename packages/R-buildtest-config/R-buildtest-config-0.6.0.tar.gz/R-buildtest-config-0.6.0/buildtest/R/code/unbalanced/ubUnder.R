library(unbalanced)
data(ubIonosphere)
n<-ncol(ubIonosphere)
output<-ubIonosphere$Class
input<-ubIonosphere[ ,-n]
data<-ubUnder(X=input, Y= output, perc = 40, method = "percPos")
newData<-cbind(data$X, data$Y)
