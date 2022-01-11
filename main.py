# Raster Processing Libraries
from osgeo import gdal
import os
import numpy as np
from function import array2raster


# Visualize Libraries
import matplotlib.pyplot as plt

# Setup Environment and Libraries For GDAL
env_path = 'C:/ProgramData/Anaconda3/envs/TriTueNhanTao/Library/share/proj'  # Change Conda Directory Here!
os.environ['PROJ_LIB'] = env_path

# Get Raster
data_path = 'Input/LANDSAT_7_Bands_30M_UTM.tif'
ds = gdal.Open(data_path, gdal.GA_ReadOnly)
data = ds.ReadAsArray()
transform = ds.GetGeoTransform()

Bands = []

# Update Band with Threshold
for k in range(ds.RasterCount):
    band_k = ds.GetRasterBand(k + 1)
    band_k = band_k.ReadAsArray()
    band_k[band_k <= -0.2] = np.nan
    Bands.append(band_k)

# Get Bands Image
blue = Bands[1]
green = Bands[2]
red = Bands[3]
nir = Bands[4]
swir1 = Bands[5]

# Calculate BSI
bsi = ((swir1 + red) - (nir + blue)) / ((swir1 + red) + (nir + blue))
bsi[bsi <= 0.0] = np.nan

# Calculate EVI
evi = 2.5 * (nir - red) / (nir + 6 * red - 7.5 * blue + 1)
evi[evi <= 0.0] = np.nan

# Calculate LSWI
lswi = (nir - swir1) / (nir + swir1)
lswi[lswi <= 0.0] = np.nan

# Calculate MNDWI
mndwi = (green - swir1) / (green + swir1)
mndwi[mndwi <= 0.0] = np.nan

# Calculate NDBI
ndbi = (swir1 - nir) / (swir1 + nir)
ndbi[ndbi <= 0.0] = np.nan

# Calculate NDVI
ndvi = (nir - red) / (nir + red)
ndvi[ndvi <= 0.0] = np.nan

# Calculate NDWI
ndwi = (green - nir) / (green + nir)
ndwi[ndwi <= 0.0] = np.nan

# Save AVI, BSI, LSWI, MNDWI, NDBI, NDVI and NDWI to New Raster
array2raster('Output/bsi.tif', transform, bsi)
array2raster('Output/evi.tif', transform, evi)
array2raster('Output/lswi.tif', transform, lswi)
array2raster('Output/mndwi.tif', transform, mndwi)
array2raster('Output/ndbi.tif', transform, ndbi)
array2raster('Output/ndvi.tif', transform, ndvi)
array2raster('Output/ndwi.tif', transform, ndwi)

# Print Statistics
for i in range(len(Bands)):
    print("Band " + str(i + 1) + ": ", np.nanmax(Bands[i]), np.nanmin(Bands[i]),
          np.nanmedian(Bands[i]), np.nanmean(Bands[i]), np.nanstd(Bands[i]))

# Debug
# plt.imshow(bsi)
# plt.show()
# plt.imshow(evi)
# plt.show()
# plt.imshow(lswi)
# plt.show()
# plt.imshow(mndwi)
# plt.show()
# plt.imshow(ndbi)
# plt.show()
# plt.imshow(ndvi)
# plt.show()
# plt.imshow(ndwi)
# plt.show()
