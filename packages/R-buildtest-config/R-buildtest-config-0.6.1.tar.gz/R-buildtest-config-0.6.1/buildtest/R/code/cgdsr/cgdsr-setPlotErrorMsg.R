library(cgdsr)
# Create CGDS object
mycgds = CGDS("http://www.cbioportal.org/")
getCancerStudies(mycgds)
# Set custom error plot message
setPlotErrorMsg(mycgds, 'My message ...')
getCancerStudies(mycgds)

