library(tm)
data("crude")
## Document access triggers the stemming function
## (i.e., all other documents are not stemmed yet)
tm_map(crude, stemDocument, lazy = TRUE)[[1]]
## Use wrapper to apply character processing function
tm_map(crude, content_transformer(tolower))
## Generate a custom transformation function which takes the heading as new content
headings <- function(x)
PlainTextDocument(meta(x, "heading"),
id = meta(x, "id"),
language = meta(x, "language"))
inspect(tm_map(crude, headings))
