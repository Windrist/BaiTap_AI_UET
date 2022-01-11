# Import Libraries
import numpy as np
import pandas as pd
import xgboost as xgb
from osgeo import gdal 
import sys
import matplotlib.pyplot as plt


# Configurations
animation = ["[□□□□□□□□□□] 0%", "[■□□□□□□□□□] 10%", "[■■□□□□□□□□] 20%", "[■■■□□□□□□□] 30%", "[■■■■□□□□□□] 40%", "[■■■■■□□□□□] 50%",
             "[■■■■■■□□□□] 60%", "[■■■■■■■□□□] 70%", "[■■■■■■■■□□] 70%", "[■■■■■■■■■□] 90%", "[■■■■■■■■■■] 100%"]
MAP_PATH = r'Input/LANDSAT_7_Bands_30M_UTM.tif'
AQUA = [77, 255, 195]
BARREN = [102, 82, 0]
CROP = [255, 255, 0]
FOREST = [0, 250, 0]
GRASS = [51, 255, 51]
RESIDENT = [250, 30, 30]
RICE = [153, 204, 0]
SCRUB = [105, 255, 105]
WATER = [0, 10, 240]
WHITE = [255, 255, 255]
COLORS = [AQUA, BARREN, CROP, FOREST, GRASS, RESIDENT, RICE, SCRUB, WATER]

# Read Rasters
ds = gdal.Open(MAP_PATH, gdal.GA_ReadOnly)
ulx, xres, xskew, uly, yskew, yres = ds.GetGeoTransform()
lrx = ulx + (ds.RasterXSize * xres)
lry = uly + (ds.RasterYSize * yres)

# Get Raster Values
Bands = []
for i in range(ds.RasterCount):
    band_k = ds.GetRasterBand(i+1)
    band_k = band_k.ReadAsArray()
    band_k[band_k <= -0.2] = np.nan
    Bands.append(band_k)
map_size = Bands[0].shape
result = np.zeros((map_size[0], map_size[1], 3), dtype=np.uint8)

# Setup XGBoost
bst = xgb.Booster({'nthread': 4})
bst.load_model('Models/best.model')

# Classify Rasters
for i in range(map_size[0]):
    for j in range(map_size[1]):
        test = []
        for b in range(ds.RasterCount):
            test.append(Bands[b][i][j])
        test = np.array([test])
        dtest = xgb.DMatrix(test)

        if np.isnan(test).any():
            result[i][j] = [0, 0, 0]
        else:
            pred = bst.predict(dtest)
            result[i][j] = COLORS[int(pred)]
        
        if j == map_size[1] - 1:
            sys.stdout.write("\r" + "Loading: {} / ".format((i+1)*(j+1)) + "{}".format(map_size[0]*map_size[1]) +
                            " | Total: " + animation[int((i+1)*(j+1)/(map_size[0]*map_size[1])*10)])
            sys.stdout.flush()

# Export Result
plt.imsave('Output/result.png', result)
plt.imshow(result)
plt.show()
