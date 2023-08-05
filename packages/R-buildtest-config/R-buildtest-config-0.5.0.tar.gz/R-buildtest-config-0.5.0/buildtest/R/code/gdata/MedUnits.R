library(gdata)
data(MedUnits)
# show available conversions
MedUnits$Measurement
# utility function
matchUnits <- function(X) MedUnits[ grep(X, MedUnits$Measurement),]
# Convert SI Glucose measurement to 'Conventional' units
GlucoseSI = c(5, 5.4, 5, 5.1, 5.6, 5.1, 4.9, 5.2, 5.5) # in SI Units
GlucoseUS = GlucoseSI / matchUnits("Glucose")$Conversion
cbind(GlucoseSI,GlucoseUS)
# also consider using ConvertMedUnits()
ConvertMedUnits( GlucoseSI, "Glucose", to="US" )
