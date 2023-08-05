library(gdata)
# iris.xls is included in the gregmisc package for use as an example
xlsfile <- file.path(path.package('gdata'),'xls','iris.xls')
xlsfile
iris <- read.xls(xlsfile) # defaults to csv format
iris <- read.xls(xlsfile,method="csv") # specify csv format
iris <- read.xls(xlsfile,method="tab") # specify tab format
head(iris) # look at the top few rows
## Not run:
## Example specifying exact Perl path for default MS-Windows install of
## ActiveState perl
iris <- read.xls(xlsfile, perl="C:/perl/bin/perl.exe")
## End(Not run)
## Not run:
## Example specifying exact Perl path for Unix systems
iris <- read.xls(xlsfile, perl="/usr/bin/perl")
## finding perl
## (read.xls automatically calls findPerl so this is rarely needed)
perl <- gdata:::findPerl("perl")
iris <- read.xls(xlsfile, perl=perl)
## End(Not run)
## Not run:
## read xls file from net
nba.url <- "http://mgtclass.mgt.unm.edu/Bose/Excel/Tutorial.05/Cases/NBA.xls"
nba <- read.xls(nba.url)
## End(Not run)
## Not run:
## read xls file ignoring all lines prior to first containing State
crime.url <- "http://www.jrsainfo.org/jabg/state_data2/Tribal_Data00.xls"
crime <- read.xls(crime.url, pattern = "State")
## use of xls2csv - open con, print two lines, close con
con <- xls2csv(crime.url)
print(readLines(con, 2))
file.remove(summary(con)$description)
## End(Not run)
## Examples demonstrating selection of specific 'sheets'
## from the example XLS file 'ExampleExcelFile.xls'
exampleFile <- file.path(path.package('gdata'),'xls',
'ExampleExcelFile.xls')
exampleFile2007 <- file.path(path.package('gdata'),'xls',
'ExampleExcelFile.xlsx')
## see the number and names of sheets:
sheetCount(exampleFile)
if( 'XLSX' %in% xlsFormats() ) ## if XLSX is supported..
sheetCount(exampleFile2007)
## show names of shets in the file
sheetNames(exampleFile)
if( 'XLSX' %in% xlsFormats() ) ## if XLSX is supported..
sheetNames(exampleFile2007)
data <- read.xls(exampleFile) ## default is first worksheet
data <- read.xls(exampleFile, sheet=2) ## second worksheet by number
data <- read.xls(exampleFile, sheet="Sheet Second",v=TRUE) ## and by name
## load the third worksheet, skipping the first two non-data lines...
if( 'XLSX' %in% xlsFormats() ) ## if XLSX is supported..
data <- read.xls(exampleFile2007, sheet="Sheet with initial text", skip=2)
## load a file containing data and column names using latin-1
## characters
latinFile <- file.path(path.package('gdata'),'xls','latin-1.xls')
latin1 <- read.xls(latinFile, fileEncoding="latin1")
colnames(latin1)

