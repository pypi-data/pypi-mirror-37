library(geiger)
geo=get(data(geospiza))
# Assuming no extinction
bd.ms(phy=geo$phy, missing=1, epsilon=0)
# Assuming high extinction
bd.ms(phy=geo$phy, missing=1, epsilon=0.9)
