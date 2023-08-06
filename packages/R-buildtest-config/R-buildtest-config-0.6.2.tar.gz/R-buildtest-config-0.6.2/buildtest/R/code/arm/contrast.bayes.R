library(arm)
cat.var <- rep(1:3, 5)
dim(contr.bayes.unordered(cat.var))
# 15*15 baseline level kept!
dim(contr.treatment(cat.var))
# 15*14
