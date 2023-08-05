library(TTR)
data(ttrc)
# Bollinger Bands
bbands <- BBands( ttrc[,c("High","Low","Close")] )
# Directional Movement Index
adx <- ADX(ttrc[,c("High","Low","Close")])
# Moving Averages
ema <- EMA(ttrc[,"Close"], n=20)
sma <- SMA(ttrc[,"Close"], n=20)
# MACD
macd <- MACD( ttrc[,"Close"] )
# RSI
rsi <- RSI(ttrc[,"Close"])
# Stochastics
stochOsc <- stoch(ttrc[,c("High","Low","Close")])
### Note: you must have a working internet connection
### for the examples below to work!
# Fetch U.S. symbols from the internet
nyseSymbols <- stockSymbols("NYSE")
# Fetch Yahoo! Finance data from the internet
ibm <- getYahooData("IBM", 19990404, 20050607)

