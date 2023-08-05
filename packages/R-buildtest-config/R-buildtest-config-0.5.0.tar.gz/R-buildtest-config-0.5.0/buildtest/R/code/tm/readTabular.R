library(tm)
df <- data.frame(contents = c("content 1", "content 2", "content 3"),
title = c("title 1" , "title 2" , "title 3" ),
authors = c("author 1" , "author 2" , "author 3" ),
topics = c("topic 1" , "topic 2" , "topic 3" ),
stringsAsFactors = FALSE)
m <- list(content = "contents", heading = "title",
author = "authors", topic = "topics")
myReader <- readTabular(mapping = m)
ds <- DataframeSource(df)
elem <- getElem(stepNext(ds))
(result <- myReader(elem, language = "en", id = "id1"))
meta(result)
