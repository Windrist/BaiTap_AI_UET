from osgeo import gdal


def array2raster(filename, transform, array):
    # Get Image Array Length
    rows, cols = array.shape

    # Create Raster
    driver = gdal.GetDriverByName('GTiff')
    out_raster = driver.Create(filename, cols, rows, 1, gdal.GDT_Float64)

    # Set Transform
    out_raster.SetGeoTransform(transform)

    # Add Image to Raster
    outband = out_raster.GetRasterBand(1)
    outband.WriteArray(array)

    # Set Coordinate System and Project
    out_raster_project = gdal.osr.SpatialReference()
    out_raster_project.ImportFromEPSG(4326)
    out_raster.SetProjection(out_raster_project.ExportToWkt())
    outband.FlushCache()
