library(cgdsr)
# Create CGDS object
mycgds = CGDS("http://www.cbioportal.org/")
getCancerStudies(mycgds)
# Activate verbose logging
setVerbose(mycgds, TRUE)
getCancerStudies(mycgds)

