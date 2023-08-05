library(gdalUtils)
gdal_setInstallation()
valid_install <- !is.null(getOption("gdalUtils_gdalPath"))
if(valid_install)
{
# Using identify mode
# Report the data format of the raster file by using the identify mode
# and specifying a data file name:
src_dataset <- system.file("external/tahoe_highrez.tif", package="gdalUtils")
gdalmanage(mode="identify",datasetname=src_dataset)
# Recursive mode will scan subfolders and report the data format:
src_dir <- system.file("external/", package="gdalUtils")
gdalmanage(mode="identify",datasetname=src_dir,r=TRUE)
## Not run:
# Using copy mode
# Copy the raster data:
file_copy <- tempfile(fileext=".tif")
gdalmanage(mode="copy",src_dataset,file_copy)
file.exists(file_copy)
# Using rename mode
# Rename the raster data:
new_name <- tempfile(fileext=".tif")
gdalmanage(mode="rename",file_copy,new_name)
file.exists(new_name)
# Using delete mode
# Delete the raster data:
gdalmanage(mode="delete",new_name)
file.exists(new_name)
## End(Not run)
}

