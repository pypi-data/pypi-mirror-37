library(ade4)
## Not run: data(tarentaise)
traits <- tarentaise$traits
ade4:::Rtoade4(traits)
# File creation traits.txt
# File creation traits_col_lab.txt
# File creation traits_row_lab.txt
# File creation traits_col_bloc.txt
# File creation traits_col_bloc_lab.txt
mil <- tarentaise$envir
ade4:::Rtoade4(mil)
#File creation mil.txt
#File creation mil_var_lab.txt
#File creation mil_moda_lab.txt
## End(Not run)

