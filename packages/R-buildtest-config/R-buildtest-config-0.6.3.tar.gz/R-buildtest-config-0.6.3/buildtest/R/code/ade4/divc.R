library(ade4)
data(ecomor)
dtaxo <- dist.taxo(ecomor$taxo)
divc(ecomor$habitat, dtaxo)
data(humDNAm)
divc(humDNAm$samples, sqrt(humDNAm$distances))

