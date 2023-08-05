library(gdata)
xlsfile <- system.file("xls", "iris.xls", package = "gdata")
xlsfile
sheetCount(xlsfile)
exampleFile <- file.path(path.package('gdata'),'xls',
'ExampleExcelFile.xls')
exampleFile2007 <- file.path(path.package('gdata'),'xls',
'ExampleExcelFile.xlsx')
sheetCount(exampleFile)
if( 'XLSX' %in% xlsFormats() ) # if XLSX is supported..
sheetNames(exampleFile2007)

