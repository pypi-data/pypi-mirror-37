library(AUC)
data(churn)
roc(churn$predictions,churn$labels)
