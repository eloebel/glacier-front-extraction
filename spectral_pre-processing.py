#!/usr/bin/python -u
#
# Purpose: Multispectral analysis of Landsat 8 Data (16bit)
# Author: Erik Loebel
# Last change: 2020-04-05
#
# To do: - full functionality for other Landsat images
#
# ------------------------------------------
import numpy as np
import sys
from tifffile import TiffFile
from osgeo import gdal
from pathlib import Path


# input informations
aq_date = (sys.argv[1])
width = 512							# adding buffer to width and height
height = 512
body = (sys.argv[2])
n_bands = 9						
range_bands=[0, 1, 2, 3, 4, 5, 6, 9, 10]

###########################
### Read landsat scenes ###
###########################
# 3 dimensional dummy array with zeros
MB_img = np.zeros((height,width,11))

# stacking up images into the array
for i in range_bands:															
	with TiffFile('/data/OUT/'+body+'/'+aq_date+'/B'+str(i+1)+'.tif') as tif:
		img = tif.asarray()
		imgarray = np.array(img)
		MB_img[:,:,i] = imgarray

	
#####################################
### Cumulative count cut in 8bit ###
#####################################
print("  - cumulative count cut 0.1 - 98 percent...")
min_percent = 0.1   # Low percentile
max_percent = 98    # High percentile


MB_img_CC_2 = np.zeros((height,width,11))
for i in range_bands:
	lo, hi = np.percentile(MB_img[:,:,i], (min_percent, max_percent))
	# Apply linear "stretch" - lo goes to 0, and hi goes to 1
	CC_img_2 = (MB_img[:,:,i].astype(float) - lo) / (hi-lo)
	# Multiply by 255, clamp range to [0, 255] and convert to uint8
	CC_img_2 = np.maximum(np.minimum(CC_img_2*255, 255), 0).astype(np.uint8)
	MB_img_CC_2[:,:,i] = CC_img_2

####################
### Export files ###
####################
print("  - exporting Gtiffs ...")
driver = gdal.GetDriverByName('Gtiff')
temp = gdal.Open('/data/OUT/'+body+'/'+aq_date+'/B1.tif')					# using B1 as template

for i in range_bands:
	dst_temp = driver.CreateCopy('/data/OUT/'+body+'/'+aq_date+'/CC_98_01_B'+str(i+1)+'_8b.tif',temp, 1)
	dst_temp.GetRasterBand(1).WriteArray(MB_img_CC_2[:,:,i])
	

