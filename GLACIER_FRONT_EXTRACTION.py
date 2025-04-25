#!/usr/bin/python -u
#
# Purpose: Glacier calving front extraction from optical landsat-8 and 9 imagery
# Author: Erik Loebel
# Last change: 2025-04-25
#
#
# ------------------------------------------

import sys
import subprocess
import shutil

glacier = str(sys.argv[1])
if glacier == 'custom':
	print("  - custom glacier: loading lon, lat coordinates", flush=True)
	lon=str(sys.argv[2])
	lat=str(sys.argv[3])

### pre processing for all scenes in folder /input ###
print('+++ INITIALIZING PRE-PROCESSING +++', flush=True)
if glacier == 'zachariae_isstrom':
	print("  - glacier is zachariae_isstrom ---> 2 seperate (and overlapping) ANN predictions neccessary", flush=True)
	subprocess.call(["scripts/pre-processing.sct", 'zachariae_isstrom_north'])
	subprocess.call(["scripts/pre-processing.sct", 'zachariae_isstrom_south'])
elif glacier == 'nioghalvfjerdsbrae':
	print("  - glacier is nioghalvfjerdsbrae ---> 3 seperate (and overlapping) ANN predictions neccessary", flush=True)
	subprocess.call(["scripts/pre-processing.sct", 'nioghalvfjerdsbrae_a'])
	subprocess.call(["scripts/pre-processing.sct", 'nioghalvfjerdsbrae_b'])
	subprocess.call(["scripts/pre-processing.sct", 'nioghalvfjerdsbrae_c'])
elif glacier == 'humboldt':
	print("  - glacier is humboldt ---> 7 seperate (and overlapping) ANN predictions neccessary", flush=True)
	subprocess.call(["scripts/pre-processing.sct", 'humboldt_a'])
	subprocess.call(["scripts/pre-processing.sct", 'humboldt_c'])
	subprocess.call(["scripts/pre-processing.sct", 'humboldt_e'])
	subprocess.call(["scripts/pre-processing.sct", 'humboldt_g'])
	subprocess.call(["scripts/pre-processing.sct", 'humboldt_i'])
	subprocess.call(["scripts/pre-processing.sct", 'humboldt_k'])
	subprocess.call(["scripts/pre-processing.sct", 'humboldt_m'])
elif glacier == 'hektoria-green-evans':
	print("  - glacier is hektoria-green-evans ---> 5 seperate (and overlapping) ANN predictions neccessary", flush=True)
	subprocess.call(["scripts/pre-processing.sct", 'humboldt_a'])
	subprocess.call(["scripts/pre-processing.sct", 'humboldt_b'])
	subprocess.call(["scripts/pre-processing.sct", 'humboldt_c'])
	subprocess.call(["scripts/pre-processing.sct", 'humboldt_d'])
	subprocess.call(["scripts/pre-processing.sct", 'humboldt_e'])
else:
	if glacier == 'custom':
		subprocess.call(["scripts/pre-processing.sct", glacier,lon,lat])
	else:
		subprocess.call(["scripts/pre-processing.sct", glacier])
print("  - pre processing finished", flush=True)

### Predicting calving front from pre processed data ###
print('+++ INITIALIZING ANN PROCESSING +++', flush=True)
subprocess.call(['python', 'scripts/predict_calving_front.py'])
shutil.rmtree("data")
