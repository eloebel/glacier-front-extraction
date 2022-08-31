#!/usr/bin/python -u
#
# Purpose: Glacier calving front extraction from optical landsat-8 and 9 imagery
# Author: Erik Loebel
# Last change: 2022-08-31
#
#
# ------------------------------------------

import numpy as np
import tensorflow as tf
from tifffile import TiffFile
from osgeo import gdal
import sys
import subprocess

glacier = str(sys.argv[1])

### pre processing for all scenes in folder /input ###
print('+++ INITIALIZING PRE-PROCESSING +++', flush=True)
if glacier == 'zachariae_isstrom':
	print("  - glacier is zachariae_isstrom ---> 2 seperate (and overlapping) ANN predictions neccessary", flush=True)
	subprocess.call(["/scripts/pre-processing.sct", 'zachariae_isstrom_north'])
	subprocess.call(["/scripts/pre-processing.sct", 'zachariae_isstrom_south'])
elif glacier == 'nioghalvfjerdsbrae':
	print("  - glacier is nioghalvfjerdsbrae ---> 3 seperate (and overlapping) ANN predictions neccessary", flush=True)
	subprocess.call(["/scripts/pre-processing.sct", 'nioghalvfjerdsbrae_a'])
	subprocess.call(["/scripts/pre-processing.sct", 'nioghalvfjerdsbrae_b'])
	subprocess.call(["/scripts/pre-processing.sct", 'nioghalvfjerdsbrae_c'])
elif glacier == 'humboldt':
	print("  - glacier is humboldt ---> 7 seperate (and overlapping) ANN predictions neccessary", flush=True)
	subprocess.call(["/scripts/pre-processing.sct", 'humboldt_a'])
	subprocess.call(["/scripts/pre-processing.sct", 'humboldt_c'])
	subprocess.call(["/scripts/pre-processing.sct", 'humboldt_e'])
	subprocess.call(["/scripts/pre-processing.sct", 'humboldt_g'])
	subprocess.call(["/scripts/pre-processing.sct", 'humboldt_i'])
	subprocess.call(["/scripts/pre-processing.sct", 'humboldt_k'])
	subprocess.call(["/scripts/pre-processing.sct", 'humboldt_m'])
else:
	subprocess.call(["/scripts/pre-processing.sct", glacier])
print("  - pre processing finished", flush=True)

### Predicting calving front from pre processed data ###
print('+++ INITIALIZING ANN PROCESSING +++', flush=True)
subprocess.call(['python', '/scripts/predict_calving_front.py'])
