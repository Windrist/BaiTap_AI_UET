# Import Libraries
import os
import pandas as pd
from osgeo import gdal
import matplotlib.pyplot as plt


# Set Input Files Path
FILE_PATH = os.listdir('Datasets/Without_Bands_Value')
MAP_PATH = r'Input/LANDSAT_7_Bands_30M_UTM.tif'
ND_PATH = os.listdir('Output')

# Read Rasters
ds = gdal.Open(MAP_PATH, gdal.GA_ReadOnly)
nd = []
for file in ND_PATH:
    nd.append(gdal.Open('Output/' + file, gdal.GA_ReadOnly))

# Get Geometry Transforms
# ulx, uly: up left (x,y)
# xres, yres: x,y scale
ulx, xres, xskew, uly, yskew, yres = ds.GetGeoTransform()
# lrx = ulx + (ds.RasterXSize * xres)
# lry = uly + (ds.RasterYSize * yres)

# Read Excel File
for file in FILE_PATH:
    df = pd.read_excel('Datasets/Without_Bands_Value/' + file, engine='openpyxl')

    x = df['X']
    y = df['Y']

    # Get 7 Band Values
    for k in range(ds.RasterCount):
        band_k = ds.GetRasterBand(k + 1)
        band_k = band_k.ReadAsArray()
        b_k = []
        for i in range(len(x)):
            pixel_x = (x[i] - ulx) / xres
            pixel_y = (y[i] - uly) / yres
            pixel_x = int(pixel_x)
            pixel_y = int(pixel_y)

            val = band_k[pixel_y][pixel_x]

            b_k.append(val)

        df_b = pd.DataFrame(b_k)
        df['Band_{}'.format(k + 1)] = df_b

    # Get NDVI, NDWI, NDBI Band Values
    for k in range(len(nd)):
        ndi = nd[k].ReadAsArray()

        b_k = []
        for i in range(len(x)):
            pixel_x = (x[i] - ulx) / xres
            pixel_y = (y[i] - uly) / yres
            pixel_x = int(pixel_x)
            pixel_y = int(pixel_y)

            val = ndi[pixel_y][pixel_x]

            b_k.append(val)

        df_b = pd.DataFrame(b_k)
        key = {0: 'BSI', 1: 'EVI', 2: 'LSWI', 3: 'MNDWI', 4: 'NDBI', 5: 'NDVI', 6: 'NDWI'}
        df['{}'.format(key[k])] = df_b

    # Export file
    df.to_excel('Datasets/Full/' + file.split('.')[0] + '_7_Bands.xlsx', index=False)
