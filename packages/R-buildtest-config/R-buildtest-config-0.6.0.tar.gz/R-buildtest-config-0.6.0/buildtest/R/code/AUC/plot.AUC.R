library(AUC)
data(churn)
plot(sensitivity(churn$predictions,churn$labels))
plot(specificity(churn$predictions,churn$labels))
plot(accuracy(churn$predictions,churn$labels))
plot(roc(churn$predictions,churn$labels))

