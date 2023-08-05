library(tm)
## An implementation for readGmane is provided as an example in ?readXML
example(readXML)
## Construct a source for a Gmane mailing list RSS feed.
GmaneSource <-
function(x)
XMLSource(x,
function(tree) {
nodes <- XML::xmlChildren(XML::xmlRoot(tree))
nodes[names(nodes) == "item"]
},
readGmane)
## Not run: gs <- GmaneSource("http://rss.gmane.org/gmane.comp.lang.r.general")
elem <- getElem(stepNext(gs))
(gmane <- readGmane(elem, language = "en", id = "id1"))
meta(gmane)
## End(Not run)
