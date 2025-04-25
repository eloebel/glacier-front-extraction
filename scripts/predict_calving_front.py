#!/usr/bin/python -u
#
# Purpose: Applying trained ANN model on pre-processed landsat imagery
# Author: Erik Loebel
# Last change: 2022-08-31
#
#
# ------------------------------------------

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')
import numpy as np
from tqdm import tqdm
from tifffile import TiffFile
import matplotlib.pyplot as plt
from osgeo import gdal
from pathlib import Path
from datetime import datetime
import subprocess
import shapefile as shp  # Requires the pyshp package
import warnings
warnings.filterwarnings("ignore")

### ------------------------------------------

# setting dimensions of input structure
RES = str(30)
IMG_WIDTH = 512
IMG_HEIGHT = 512
IMG_CHANNELS = 9	
NN_DEPTH = 6
kernel_size = 3      

# getting start date for file naming
today = datetime.now()
d_start = today.strftime("%Y%m%d_%H:%M")

# setting PATH variables
INPUT_PATH = 'data/OUT' 
OUTPUT_PATH = ('input/PRED_' + str(d_start))
WEIGHT_PATH = ('model-weights.tf')

### ------------------------------------------
# Building the model ###
inputs = tf.keras.layers.Input((IMG_WIDTH, IMG_HEIGHT, IMG_CHANNELS))
s = tf.keras.layers.Lambda(lambda x: x / 255)(inputs)                           # convert uint8 to float

if NN_DEPTH == 6:
	print('  - Loeading U-Net depth 6')
	# Contraction path
	c1 = tf.keras.layers.Conv2D(32, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same')(s)
	c1 = tf.keras.layers.BatchNormalization()(c1)
	c1 = tf.keras.layers.Activation('relu')(c1)
	c1 = tf.keras.layers.Conv2D(32, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same')(c1)
	p1 = tf.keras.layers.MaxPooling2D((2,2))(c1)

	c2 = tf.keras.layers.Conv2D(64, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same')(p1)
	c2 = tf.keras.layers.BatchNormalization()(c2)
	c2 = tf.keras.layers.Activation('relu')(c2)
	c2 = tf.keras.layers.Conv2D(64, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same')(c2)
	p2 = tf.keras.layers.MaxPooling2D((2,2))(c2)

	c3 = tf.keras.layers.Conv2D(128, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same', use_bias=False)(p2)
	c3 = tf.keras.layers.BatchNormalization()(c3)
	c3 = tf.keras.layers.Activation('relu')(c3)
	c3 = tf.keras.layers.Conv2D(128, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same', use_bias=False)(c3)
	p3 = tf.keras.layers.MaxPooling2D((2,2))(c3)

	c4 = tf.keras.layers.Conv2D(256, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same', use_bias=False)(p3)
	c4 = tf.keras.layers.BatchNormalization()(c4)
	c4 = tf.keras.layers.Activation('relu')(c4)
	c4 = tf.keras.layers.Conv2D(256, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same', use_bias=False)(c4)
	p4 = tf.keras.layers.MaxPooling2D((2,2))(c4)

	c5 = tf.keras.layers.Conv2D(512, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same', use_bias=False)(p4)
	c5 = tf.keras.layers.BatchNormalization()(c5)
	c5 = tf.keras.layers.Activation('relu')(c5)
	c5 = tf.keras.layers.Conv2D(512, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same', use_bias=False)(c5)
	p5 = tf.keras.layers.MaxPooling2D((2,2))(c5)

	c6 = tf.keras.layers.Conv2D(1024, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same', use_bias=False)(p5)
	c6 = tf.keras.layers.BatchNormalization()(c6)
	c6 = tf.keras.layers.Activation('relu')(c6)
	c6 = tf.keras.layers.Conv2D(1024, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same', use_bias=False)(c6)
	p6 = tf.keras.layers.MaxPooling2D((2,2))(c6)

	c7 = tf.keras.layers.Conv2D(2048, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same', use_bias=False)(p6)
	c7 = tf.keras.layers.BatchNormalization()(c7)
	c7 = tf.keras.layers.Activation('relu')(c7)
	c7 = tf.keras.layers.Conv2D(2048, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same', use_bias=False)(c7)

	# Expansion path
	u8 = tf.keras.layers.Conv2DTranspose(1024, (2,2), strides=(2,2), padding='same')(c7)
	u8 = tf.keras.layers.concatenate([u8, c6])
	c8 = tf.keras.layers.Conv2D(1024, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same', use_bias=False)(u8)
	c8 = tf.keras.layers.BatchNormalization()(c8)
	c8 = tf.keras.layers.Activation('relu')(c8)
	c8 = tf.keras.layers.Conv2D(1024, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same', use_bias=False)(c8)

	u9 = tf.keras.layers.Conv2DTranspose(512, (2,2), strides=(2,2), padding='same')(c8)
	u9 = tf.keras.layers.concatenate([u9, c5])
	c9 = tf.keras.layers.Conv2D(512, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same', use_bias=False)(u9)
	c9 = tf.keras.layers.BatchNormalization()(c9)
	c9 = tf.keras.layers.Activation('relu')(c9)
	c9 = tf.keras.layers.Conv2D(512, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same', use_bias=False)(c9)

	u10 = tf.keras.layers.Conv2DTranspose(256, (2,2), strides=(2,2), padding='same')(c9)
	u10 = tf.keras.layers.concatenate([u10, c4])
	c10 = tf.keras.layers.Conv2D(256, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same', use_bias=False)(u10)
	c10 = tf.keras.layers.BatchNormalization()(c10)
	c10 = tf.keras.layers.Activation('relu')(c10)
	c10 = tf.keras.layers.Conv2D(256, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same', use_bias=False)(c10)

	u11 = tf.keras.layers.Conv2DTranspose(128, (2,2), strides=(2,2), padding='same')(c10)
	u11 = tf.keras.layers.concatenate([u11, c3])
	c11 = tf.keras.layers.Conv2D(128, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same', use_bias=False)(u11)
	c11 = tf.keras.layers.BatchNormalization()(c11)
	c11 = tf.keras.layers.Activation('relu')(c11)
	c11 = tf.keras.layers.Conv2D(128, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same', use_bias=False)(c11)

	u12 = tf.keras.layers.Conv2DTranspose(64, (2,2), strides=(2,2), padding='same')(c11)
	u12 = tf.keras.layers.concatenate([u12, c2])
	c12 = tf.keras.layers.Conv2D(64, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same', use_bias=False)(u12)
	c12 = tf.keras.layers.BatchNormalization()(c12)
	c12 = tf.keras.layers.Activation('relu')(c12)
	c12 = tf.keras.layers.Conv2D(64, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same', use_bias=False)(c12)

	u13 = tf.keras.layers.Conv2DTranspose(32, (2,2), strides=(2,2), padding='same')(c12)
	u13 = tf.keras.layers.concatenate([u13, c1])
	c13 = tf.keras.layers.Conv2D(32, (kernel_size,kernel_size), kernel_initializer='he_normal', padding='same', use_bias=False)(u13)
	c13 = tf.keras.layers.BatchNormalization()(c13)
	c13 = tf.keras.layers.Activation('relu')(c13)
	c13 = tf.keras.layers.Conv2D(32, (kernel_size,kernel_size), activation='relu', kernel_initializer='he_normal', padding='same', use_bias=False)(c13)

	outputs = tf.keras.layers.Conv2D(1, (1,1), activation='sigmoid')(c13)

model = tf.keras.Model(inputs=[inputs], outputs=[outputs])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Restore the weights
print('  - Restoring model weights')
model_2 = tf.keras.models.load_model(WEIGHT_PATH)

# generating lits of test ids
test_bodies = next(os.walk(INPUT_PATH))[1]
test_ids = []
for i in range(len(test_bodies)):
	test_ids.extend(next(os.walk((INPUT_PATH +'/'+ test_bodies[i])))[1])

# Creating output structure
Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)
driver = gdal.GetDriverByName('Gtiff')

print('  - Predicting calving fronts from pre-processed input')
for i, body in tqdm(enumerate(test_bodies), total=len(test_bodies)): 
    test_id_temp = next(os.walk(INPUT_PATH + '/'+ body))[1]
    #print('      ... %s' % (body))
    for n in range(len(test_id_temp)):
        #print('      ... %s ... %s' % (body,test_id_temp[n]))
        X_test = np.zeros((IMG_HEIGHT, IMG_WIDTH, IMG_CHANNELS), dtype=np.uint8)
        with TiffFile(INPUT_PATH +'/'+ body + '/' +test_id_temp[n] + '/CC_98_01_B1_8b.tif') as tif:
              img = tif.asarray()
              imgarray = (np.array(img)).astype('uint8')
              X_test[:,:,0] = imgarray
            
        with TiffFile(INPUT_PATH +'/'+ body + '/' +test_id_temp[n] + '/CC_98_01_B2_8b.tif') as tif:
              img = tif.asarray()
              imgarray = (np.array(img)).astype('uint8')
              X_test[:,:,1] = imgarray
            
        with TiffFile(INPUT_PATH +'/'+ body + '/' +test_id_temp[n] + '/CC_98_01_B3_8b.tif') as tif:
              img = tif.asarray()
              imgarray = (np.array(img)).astype('uint8')
              X_test[:,:,2] = imgarray
            
        with TiffFile(INPUT_PATH +'/'+ body + '/' +test_id_temp[n] + '/CC_98_01_B4_8b.tif') as tif:
              img = tif.asarray()
              imgarray = (np.array(img)).astype('uint8')
              X_test[:,:,3] = imgarray
            
        with TiffFile(INPUT_PATH +'/'+ body + '/' +test_id_temp[n] + '/CC_98_01_B5_8b.tif') as tif:
              img = tif.asarray()
              imgarray = (np.array(img)).astype('uint8')
              X_test[:,:,4] = imgarray
            
        with TiffFile(INPUT_PATH +'/'+ body + '/' +test_id_temp[n] + '/CC_98_01_B6_8b.tif') as tif:
              img = tif.asarray()
              imgarray = (np.array(img)).astype('uint8')
              X_test[:,:,5] = imgarray
            
        with TiffFile(INPUT_PATH +'/'+ body + '/' +test_id_temp[n] + '/CC_98_01_B7_8b.tif') as tif:
              img = tif.asarray()
              imgarray = (np.array(img)).astype('uint8')
              X_test[:,:,6] = imgarray
              
        with TiffFile(INPUT_PATH +'/'+ body + '/' +test_id_temp[n] + '/CC_98_01_B10_8b.tif') as tif:
              img = tif.asarray()
              imgarray = (np.array(img)).astype('uint8')
              X_test[:,:,7] = imgarray
            
        with TiffFile(INPUT_PATH +'/'+ body + '/' +test_id_temp[n] + '/CC_98_01_B11_8b.tif') as tif:
              img = tif.asarray()
              imgarray = (np.array(img)).astype('uint8')
              X_test[:,:,8] = imgarray

        # Predict input data
        X_test = X_test[np.newaxis,:,:,:]
        pred = model_2.predict(X_test,  verbose=2)
        
        # saving prediction of test data
        Path(OUTPUT_PATH + '/' + body + '/' + test_id_temp[n]).mkdir(parents=True, exist_ok=True)
        temp = gdal.Open(INPUT_PATH + '/'+ body + '/' + test_id_temp[n] +'/CC_98_01_B1_8b.tif')
		# save .tif of prediction (float)
        dst_temp = driver.CreateCopy(OUTPUT_PATH + '/' + body + '/' + test_id_temp[n] + '/pred_' +test_id_temp[n]+'.tif', temp, 1)
        dst_temp.GetRasterBand(1).WriteArray(((np.squeeze(pred))*99)+1)
        del dst_temp, temp
      
# vectorizing prediction
print('  - Vectorization')
rc = subprocess.call(["scripts/vectorize_prediction.sct", OUTPUT_PATH])


# MERGE subregions (Zachariae isstrom, Humboldt, Nioghalvfjerdsbrae) ------> ONLY WORKS IF SAME SCENES IN SUBREGION
if 'zachariae_isstrom_north' and 'zachariae_isstrom_south' in test_bodies :
    print('  - Merging predictions for Zachariae Isstrom')
    GLACIER_NUMBER = 1
    # merge_prediction performs merging + vectorization
    subprocess.call(['python', 'scripts/merge_prediction.py', INPUT_PATH, OUTPUT_PATH, str(GLACIER_NUMBER)])

if 'humboldt_a' and 'humboldt_c' and 'humboldt_e' and 'humboldt_g' and 'humboldt_i' and 'humboldt_k' and 'humboldt_m' in test_bodies :
    print('  - Merging predictions for Humboldt')
    GLACIER_NUMBER = 2
    subprocess.call(['python', 'scripts/merge_prediction.py', INPUT_PATH, OUTPUT_PATH, str(GLACIER_NUMBER)])

if 'nioghalvfjerdsbrae_a' and 'nioghalvfjerdsbrae_b' and 'nioghalvfjerdsbrae_c' in test_bodies :
    print('  - Merging predictions for Nioghalvfjerdsbrae')
    GLACIER_NUMBER = 3
    subprocess.call(['python', 'scripts/merge_prediction.py', INPUT_PATH, OUTPUT_PATH, str(GLACIER_NUMBER)])

if 'hektoria-green-evans_a' and 'hektoria-green-evans_b' and 'hektoria-green-evans_c' and 'hektoria-green-evans_d' and 'hektoria-green-evans_e' and 'hektoria-green-evans_f' in test_bodies :
    print('  -- Merging predictions for Hektoria-Green-Evans')
    GLACIER_NUMBER = 4
    subprocess.call(['python', 'scripts/merge_prediction.py', INPUT_PATH, OUTPUT_PATH, str(GLACIER_NUMBER)])

test_bodies_merged = next(os.walk(OUTPUT_PATH))[1]       # define new test_bodies to integrate merged basins and remove subbasins

# MASK static coastline
print('  - Masking static coastline')
for i, body in tqdm(enumerate(test_bodies_merged), total=len(test_bodies_merged)):
	if body == 'drygalski' or body == 'waltershausen_glacier' or body == 'store' or body == 'rinks_isbrae' or body == 'ingia_isbrae' or body == 'daugaard_jensen' or body =='humboldt' or body =='jakobshavn_isbrae' or body =='helheim' or body =='rinks_isbrae' or body =='hagen_brae' or body =='ryder_glacier' or body =='zachariae_isstrom' or body =='harald_moltke_brae' or body =='academy' or body =='sverdrup':
		n_fronts = 1
		# masking prediction
		mask_gdal = subprocess.call(["scripts/mask_coastline.sct", OUTPUT_PATH, str(body), str(n_fronts)])
	elif body == 'tracy_gletscher' or body == 'kangiata_nunaata_sermia' or body == 'docker_smith' or body == 'kangerdlugssuaq' or body == 'tracy_gletscher' or body =='eqip_sermia_region':
		n_fronts = 2
		# masking prediction
		mask_gdal = subprocess.call(["scripts/mask_coastline.sct", OUTPUT_PATH, str(body), str(n_fronts)])
	elif body =='boydell' or body == 'nioghalvfjerdsbrae' or body == 'hayes':
		n_fronts = 3
		# masking prediction
		mask_gdal = subprocess.call(["scripts/mask_coastline.sct", OUTPUT_PATH, str(body), str(n_fronts)])
	elif body == 'kong_oscar' or body == 'upernavik_isstrom_north':
		n_fronts = 4
		# masking prediction
		mask_gdal = subprocess.call(["scripts/mask_coastline.sct", OUTPUT_PATH, str(body), str(n_fronts)])
    
# creating overview plot
print('  - Creating overview plots')
for i, body in tqdm(enumerate(test_bodies), total=len(test_bodies)): 
    if body != 'zachariae_isstrom' or body != 'nioghalvfjerdsbrae' or body != 'humboldt':
        test_id_temp = next(os.walk(INPUT_PATH + '/'+ body))[1]
        Path(OUTPUT_PATH + '/' + body ).mkdir(parents=True, exist_ok=True)
        for n in range(len(test_id_temp)):		
        
            # load rgb image
            with TiffFile(INPUT_PATH + '/'+ body + '/' + test_id_temp[n] +'/CC_98_01_B2_8b.tif') as tif:
                img_1_B2 = tif.asarray()
            with TiffFile(INPUT_PATH + '/'+ body + '/' + test_id_temp[n] +'/CC_98_01_B3_8b.tif') as tif:
                img_1_B3 = tif.asarray()
            with TiffFile(INPUT_PATH + '/'+ body + '/' + test_id_temp[n] +'/CC_98_01_B4_8b.tif') as tif:
                img_1_B4 = tif.asarray()            
            img_1_RGB = np.zeros((512,512,3))   
            img_1_RGB[:,:,0] = img_1_B4
            img_1_RGB[:,:,1] = img_1_B3
            img_1_RGB[:,:,2] = img_1_B2
            img_1_max= np.max(img_1_RGB)
        
            # loading .shp file
            sf = shp.Reader(OUTPUT_PATH + '/' + body + '/' + test_id_temp[n] + '/calving_front_' +test_id_temp[n]+'.shp')
            for shape in sf.shapeRecords():
                x = [j[0] for j in shape.shape.points[:]]
                y = [j[1] for j in shape.shape.points[:]]
        
            # getting scene extend
            temp = gdal.Open(INPUT_PATH + '/'+ body + '/' + test_id_temp[n] +'/CC_98_01_B1_8b.tif')
            width = temp.RasterXSize
            height = temp.RasterYSize
            gt = temp.GetGeoTransform()
            minx = gt[0]
            miny = gt[3] + width*gt[4] + height*gt[5] 
            maxx = gt[0] + width*gt[1] + height*gt[2]
            maxy = gt[3] 
            img_extent = (minx, maxx, miny, maxy) 
        
		# plotting predictions for test dataset
            with TiffFile(INPUT_PATH +'/'+ body + '/' +test_id_temp[n] + '/CC_98_01_B1_8b.tif') as tif:
                  img = tif.asarray()
                  imgarray = (np.array(img)).astype('uint8')
            with TiffFile(OUTPUT_PATH + '/' + body + '/' + test_id_temp[n] + '/pred_' +test_id_temp[n]+'.tif') as tif:
                  pred = tif.asarray()
                  predarray = (np.array(pred)).astype('uint8')
              
            fig,axes = plt.subplots(1,2,figsize=(30,15),sharex='all', sharey='all')
            fig.subplots_adjust(wspace=0.1, hspace=0.15)

            #axes[0].imshow(imgarray,extent=img_extent,cmap='gray')                              # B1
            axes[0].imshow(((img_1_RGB[:,:,0:3])/img_1_max),extent=img_extent,cmap='gray')      # RGB
            axes[0].set_title('Enhanced RGB composit Scene '+test_id_temp[n],fontsize=25)
            axes[0].plot(x,y, color='b',linewidth=3)
            if body == 'kong_oscar' or body == 'upernavik_isstrom_north' or body =='boydell' or body == 'hayes' or body == 'tracy_gletscher' or body == 'kangiata_nunaata_sermia' or body == 'docker_smith' or body == 'kangerdlugssuaq' or body == 'tracy_gletscher' or body =='eqip_sermia_region' or body == 'drygalski' or body == 'waltershausen_glacier' or body == 'store' or body == 'rinks_isbrae' or body == 'ingia_isbrae' or body == 'daugaard_jensen' or body =='jakobshavn_isbrae' or body =='helheim' or body =='rinks_isbrae' or body =='hagen_brae' or body =='ryder_glacier' or body =='harald_moltke_brae' or body =='academy' or body =='sverdrup':
                sf_masked = shp.Reader(OUTPUT_PATH + '/' + body + '/' + test_id_temp[n] + '/calving_front_' +test_id_temp[n]+'_masked.shp')
                for shape in sf_masked.shapeRecords():
                    x_masked = [j[0] for j in shape.shape.points[:]]
                    y_masked = [j[1] for j in shape.shape.points[:]]
                    axes[0].plot(x_masked,y_masked, color='r',linewidth=3, label='Masked vectorized front')
            axes[0].axis('off')

            p1=axes[1].imshow(np.squeeze(predarray),extent=img_extent,cmap='gray')
            axes[1].set_title('Classification result (white: Land/Ice | black: ocean)',fontsize=25)
            axes[1].plot(x,y, color='b',linewidth=3, label='Vectorized prediction')
            axes[1].axis('off')
            if body == 'kong_oscar' or body == 'upernavik_isstrom_north' or body =='boydell' or body == 'hayes' or body == 'tracy_gletscher' or body == 'kangiata_nunaata_sermia' or body == 'docker_smith' or body == 'kangerdlugssuaq' or body == 'tracy_gletscher' or body =='eqip_sermia_region' or body == 'drygalski' or body == 'waltershausen_glacier' or body == 'store' or body == 'rinks_isbrae' or body == 'ingia_isbrae' or body == 'daugaard_jensen' or body =='jakobshavn_isbrae' or body =='helheim' or body =='rinks_isbrae' or body =='hagen_brae' or body =='ryder_glacier' or body =='harald_moltke_brae' or body =='academy' or body =='sverdrup':
                sf_masked = shp.Reader(OUTPUT_PATH + '/' + body + '/' + test_id_temp[n] + '/calving_front_' +test_id_temp[n]+'_masked.shp')
                for shape in sf_masked.shapeRecords():
                    x_masked = [j[0] for j in shape.shape.points[:]]
                    y_masked = [j[1] for j in shape.shape.points[:]]
                    axes[1].plot(x_masked,y_masked, color='r',linewidth=3, label='Masked vectorized front')     

            plt.savefig(OUTPUT_PATH + '/' + body + '/' + test_id_temp[n] + '/OVERVIEW_' +test_id_temp[n]+'.png')
            plt.close()
