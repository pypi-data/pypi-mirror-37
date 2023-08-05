library(TTR)
data(ttrc)
dc <- DonchianChannel( ttrc[,c("High","Low")] )
