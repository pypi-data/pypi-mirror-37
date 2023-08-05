library(tm)
data("crude")
TermDocumentMatrix(crude,
control = list(removePunctuation = TRUE,
stopwords = TRUE,
weighting = function(x)
weightSMART(x, spec = "ntc")))
