library(TTR)
data(ttrc)
volatility <- chaikinVolatility(ttrc[,c("High","Low")])
