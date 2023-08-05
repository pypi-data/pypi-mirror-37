library(ape)
## a small extract from data(woddmouse) in sequential format:
cat("3 40",
"No305 NTTCGAAAAACACACCCACTACTAAAANTTATCAGTCACT",
"No304 ATTCGAAAAACACACCCACTACTAAAAATTATCAACCACT",
"No306 ATTCGAAAAACACACCCACTACTAAAAATTATCAATCACT",
file = "exdna.txt", sep = "\n")
ex.dna <- read.dna("exdna.txt", format = "sequential")
str(ex.dna)
ex.dna
## the same data in interleaved format...
cat("3 40",
"No305 NTTCGAAAAA CACACCCACT",
"No304 ATTCGAAAAA CACACCCACT",
"No306 ATTCGAAAAA CACACCCACT",
" ACTAAAANTT ATCAGTCACT",
" ACTAAAAATT ATCAACCACT",
" ACTAAAAATT ATCAATCACT",
file = "exdna.txt", sep = "\n")
ex.dna2 <- read.dna("exdna.txt")
## ... in clustal format...
cat("CLUSTAL (ape) multiple sequence alignment", "",
"No305 NTTCGAAAAACACACCCACTACTAAAANTTATCAGTCACT",
"No304 ATTCGAAAAACACACCCACTACTAAAAATTATCAACCACT",
"No306 ATTCGAAAAACACACCCACTACTAAAAATTATCAATCACT",
" ************************** ****** ****",
file = "exdna.txt", sep = "\n")
ex.dna3 <- read.dna("exdna.txt", format = "clustal")
## ... and in FASTA format
cat(">No305",
"NTTCGAAAAACACACCCACTACTAAAANTTATCAGTCACT",
">No304",
"ATTCGAAAAACACACCCACTACTAAAAATTATCAACCACT",
">No306",
"ATTCGAAAAACACACCCACTACTAAAAATTATCAATCACT",
file = "exdna.fas", sep = "\n")
ex.dna4 <- read.dna("exdna.fas", format = "fasta")
## They are the same:
identical(ex.dna, ex.dna2)
identical(ex.dna, ex.dna3)
identical(ex.dna, ex.dna4)
## How to read compressed files:
## create the ZIP file:
zip("exdna.fas.zip", "exdna.fas")
## create the GZ file with a connection:
con <- gzfile("exdna.fas.gz", "wt")
cat(">No305", "NTTCGAAAAACACACCCACTACTAAAANTTATCAGTCACT",
">No304", "ATTCGAAAAACACACCCACTACTAAAAATTATCAACCACT",
">No306", "ATTCGAAAAACACACCCACTACTAAAAATTATCAATCACT",
file = con, sep = "\n")
close(con)
ex.dna5 <- read.dna(unz("exdna.fas.zip", "exdna.fas"), "fasta")
ex.dna6 <- read.dna(gzfile("exdna.fas.gz"), "fasta")
identical(ex.dna5, ex.dna4)
identical(ex.dna6, ex.dna4)
unlink("exdna.txt") # clean-up
unlink("exdna.fas") # clean-up
unlink("exdna.fas.zip")
unlink("exdna.fas.gz")
## read a FASTQ file from 1000 Genomes:
## Not run:
a <- "ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/phase3/data/HG00096/sequence_read/"
b <- "SRR062641.filt.fastq.gz"
URL <- paste0(a, b)
download.file(URL, b)
X <- read.fastq(b)
X # 109,811 sequences
## get the qualities of the first sequence:
(qual1 <- attr(X, "QUAL")[[1]])
## the corresponding probabilities:
10^(-qual1/10)
## get the mean quality for each sequence:
mean.qual <- sapply(attr(X, "Q"), mean)
## can do the same for var, sd, ...
## End(Not run)

