library(ape)
## Not run:
## requires to be connected on Internet
d <- "ftp://ftp.ensembl.org/pub/release-86/gff3/homo_sapiens/"
f <- "Homo_sapiens.GRCh38.86.chromosome.MT.gff3.gz"
download.file(paste0(d, f), "mt_gff3.gz")
gff.mito <- read.gff("mt_gff3.gz")
## the lengths of the sequence features:
gff.mito$end - (gff.mito$start - 1)
table(gff.mito$type)
## where the exons start:
gff.mito$start[gff.mito$type == "exon"]
## End(Not run)
