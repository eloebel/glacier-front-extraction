#!/usr/bin/python -u
#
# Purpose: Merge predictions for Zachariae Isstroem, Nioghalvfjerdsbrae and Humbold glacier
# Author: Erik Loebel
# Last change: 2022-08-31
#
#
# ------------------------------------------

import os
import sys
from pathlib import Path
import subprocess

### ------------------------------------------
INPUT_PATH = str(sys.argv[1])                      			
OUTPUT_PATH = str(sys.argv[2])            				             
GLACIER_NUMBER = int((sys.argv[3]))
### ------------------------------------------

if GLACIER_NUMBER == 1:
    Path(OUTPUT_PATH + '/zachariae_isstrom').mkdir(parents=True, exist_ok=True)      
    ids = next(os.walk(OUTPUT_PATH + '/zachariae_isstrom_north'))[1]       # später: nur ids die in beiden ordner sind
   
    for n in range(len(ids)):
        Path(OUTPUT_PATH + '/zachariae_isstrom/' + ids[n]).mkdir(parents=True, exist_ok=True)
        Path(OUTPUT_PATH + '/zachariae_isstrom/' + ids[n] + '/TEMP').mkdir(parents=True, exist_ok=True)
    
        pred_north=OUTPUT_PATH + '/zachariae_isstrom_north/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_south=OUTPUT_PATH + '/zachariae_isstrom_south/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        temp_folder=OUTPUT_PATH + '/zachariae_isstrom/' + ids[n] + '/TEMP'
        # GDAL operation include merging + vectorization
        proc_gdal = subprocess.call(["scripts/gdal_operations_zachariae.sct", temp_folder, pred_north, pred_south,ids[n]])
    # deleting subfolders

if GLACIER_NUMBER == 2:
    Path(OUTPUT_PATH + '/humboldt').mkdir(parents=True, exist_ok=True)      
    ids = next(os.walk(OUTPUT_PATH + '/humboldt_a'))[1]       # später: nur ids die in allen ordner sind
   
    for n in range(len(ids)):
        Path(OUTPUT_PATH + '/humboldt/' + ids[n]).mkdir(parents=True, exist_ok=True)
        Path(OUTPUT_PATH + '/humboldt/' + ids[n] + '/TEMP').mkdir(parents=True, exist_ok=True)
    
        pred_a=OUTPUT_PATH + '/humboldt_a/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_c=OUTPUT_PATH + '/humboldt_c/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_e=OUTPUT_PATH + '/humboldt_e/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_g=OUTPUT_PATH + '/humboldt_g/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_i=OUTPUT_PATH + '/humboldt_i/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_k=OUTPUT_PATH + '/humboldt_k/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_m=OUTPUT_PATH + '/humboldt_m/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        temp_folder=OUTPUT_PATH + '/humboldt/' + ids[n] + '/TEMP'
        # GDAL operation include merging + vectorization
        proc_gdal = subprocess.call(["scripts/gdal_operations_humboldt.sct", temp_folder, pred_a, pred_c, pred_e, pred_g, pred_i, pred_k, pred_m,ids[n]])
        
if GLACIER_NUMBER == 3:
    Path(OUTPUT_PATH + '/nioghalvfjerdsbrae').mkdir(parents=True, exist_ok=True)      
    ids = next(os.walk(OUTPUT_PATH + '/nioghalvfjerdsbrae_a'))[1]       # später: nur ids die in allen ordner sind
    for n in range(len(ids)):
        Path(OUTPUT_PATH + '/nioghalvfjerdsbrae/' + ids[n]).mkdir(parents=True, exist_ok=True)
        Path(OUTPUT_PATH + '/nioghalvfjerdsbrae/' + ids[n] + '/TEMP').mkdir(parents=True, exist_ok=True)
    
        pred_a=OUTPUT_PATH + '/nioghalvfjerdsbrae_a/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_b=OUTPUT_PATH + '/nioghalvfjerdsbrae_b/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_c=OUTPUT_PATH + '/nioghalvfjerdsbrae_c/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        temp_folder=OUTPUT_PATH + '/nioghalvfjerdsbrae/' + ids[n] + '/TEMP'
        # GDAL operation include merging + vectorization
        proc_gdal = subprocess.call(["scripts/gdal_operations_nioghalvfjerdsbrae.sct", temp_folder, pred_a, pred_b, pred_c, ids[n]])

if GLACIER_NUMBER == 4:
    Path(OUTPUT_PATH + '/hektoria-green-evans').mkdir(parents=True, exist_ok=True)      
    ids = next(os.walk(OUTPUT_PATH + '/hektoria-green-evans_a'))[1]       # später: nur ids die in allen ordner sind
    for n in range(len(ids)):
        print('      ... %s' % (ids[n]))
        Path(OUTPUT_PATH + '/hektoria-green-evans/' + ids[n]).mkdir(parents=True, exist_ok=True)
        Path(OUTPUT_PATH + '/hektoria-green-evans/' + ids[n] + '/TEMP').mkdir(parents=True, exist_ok=True)
    
        pred_a=OUTPUT_PATH + '/hektoria-green-evans_a/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_b=OUTPUT_PATH + '/hektoria-green-evans_b/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_c=OUTPUT_PATH + '/hektoria-green-evans_c/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_d=OUTPUT_PATH + '/hektoria-green-evans_d/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        pred_e=OUTPUT_PATH + '/hektoria-green-evans_e/'+ ids[n] +'/pred_'+ ids[n] +'.tif'
        temp_folder=OUTPUT_PATH + '/hektoria-green-evans/' + ids[n] + '/TEMP'
        # GDAL operation include merging + vectorization
        proc_gdal = subprocess.call(["scripts/gdal_operations_hektoria-green-evans.sct", temp_folder, pred_a, pred_b, pred_c, pred_d, pred_e,ids[n]])
