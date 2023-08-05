library(gdalUtils)
## Not run:
input_folder <- system.file("external",package="gdalUtils")
list.files(input_folder,pattern=".tif")
output_folder <- tempdir()
# library(spatial.tools)
# sfQuickInit() # from package spatial.tools to launch a parallel PSOCK cluster
batch_gdal_translate(infiles=input_folder,outdir=output_folder,
outsuffix="_converted.envi",of="ENVI",pattern=".tif$")
list.files(output_folder,pattern="_converted.envi$")
# sfQuickStop() # from package spatial.tools to stop a parallel PSOCK cluster
## End(Not run)
