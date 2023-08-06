library(cgdsr)
# Create CGDS object
mycgds = CGDS("http://www.cbioportal.org/")
# Test the CGDS endpoint URL using a few simple API tests
test(mycgds)
# Get list of cancer studies at server
getCancerStudies(mycgds)

