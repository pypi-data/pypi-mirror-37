library(cgdsr)
# Create CGDS object
mycgds = CGDS("http://www.cbioportal.org/")
getCancerStudies(mycgds)
# Get available case lists (collection of samples) for a given cancer study
# Get Extended Mutation Data for EGFR and PTEN in TCGA GBM
#
# getMutationData(mycgds,gbm_tcga_all,gbm_tcga_mutations,c('EGFR','PTEN'))
