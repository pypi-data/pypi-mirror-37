library(cgdsr)
# Create CGDS object
mycgds = CGDS("http://www.cbioportal.org/")
# Run tests
test(mycgds)
