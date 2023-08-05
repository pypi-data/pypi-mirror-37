library(tm)
readGmane <- 
readXML(spec = list(author = list("node", "/item/creator"),
	content = list("node", "/item/description"),
	datetimestamp = list("function", function(node)
	strptime(sapply(XML::getNodeSet(node, "/item/date"), XML::xmlValue),
		format = "%Y-%m-%dT%H:%M:%S",
		tz = "GMT")),
	description = list("unevaluated", ""),
	heading = list("node", "/item/title"),
	id = list("node", "/item/link"),
	origin = list("unevaluated", "Gmane Mailing List Archive")),
	doc = PlainTextDocument())
