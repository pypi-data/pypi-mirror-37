library(chron)
dts <- dates("01/01/98") + trunc(365 * runif(50))
table(is.weekend(dts))
.Holidays
# New Year Memorial Indepen. Labor day Thanksgiving Christmas
# 01/01/92 05/25/92 07/04/92 09/07/92 11/26/92 12/25/92
# NOTE: Only these 6 holidays from 1992 are defined by default!
