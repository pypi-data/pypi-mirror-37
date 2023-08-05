library(gdalUtils)
## Not run:
# Assumes you have GDAL installed on your local machine.
getOption("gdalUtils_gdalPath")
gdal_setInstallation()
getOption("gdalUtils_gdalPath")
# If there is more than one installation of GDAL, this is the
# most recent installation:
getOption("gdalUtils_gdalPath")[[1]]
# The version number:
getOption("gdalUtils_gdalPath")[[1]]$version
## End(Not run)
