library(tm)
data("crude")
crude[[1]]
removeWords(crude[[1]], stopwords("english"))
