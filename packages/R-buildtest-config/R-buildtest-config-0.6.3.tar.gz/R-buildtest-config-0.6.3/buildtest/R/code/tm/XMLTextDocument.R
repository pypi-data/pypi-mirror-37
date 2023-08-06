library(tm)
xml <- system.file("exampleData", "test.xml", package = "XML")
(xtd <- XMLTextDocument(XML::xmlTreeParse(xml),
heading = "XML text document",
id = xml,
language = "en"))
meta(xtd)
as.character(xtd)
