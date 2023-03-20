# Automated calving front delineation from multispectral satellite imagery using deep learning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This software automatically delineates calving front positions from Landsat-8 and Landsat-9 Level-1 data archives. It processes multispectral imagery using a specialized neural network. In particular, it uses a convolutional neural network of the U-Net architecture to semantically segment images into a glacier/land and water class. The glacier calving front, which is described by the boundary between these two classes, is then extracted by vectorizing and masking the model prediction. The figure below gives a broad overview of the processing workflow.

![workflow_v5](https://user-images.githubusercontent.com/68990782/225638941-61c5c4ca-3319-4894-92aa-f81d853dbf15.png)

Model is trained using manually delineated calving front position from 19 Greenland glaciers. We evaluated the performance of this model using three independent test datasets, including glaciers in Svalbard, at the Antarctic Peninsula and in Patagonia. The quality of the automatically extracted calving fronts is comparable to that of manually delineated calving fronts. The processing system and its validation are described in detail in [this article](https://doi.org/10.1109/TGRS.2022.3208454).

## Usage
We provide three options for using this software. We recommend using the containerized implementation via Docker (Option 1) or Singularity (Option 2). Also possible to use our source code directly (Option 3).
### Option 1: Docker
Tested for verison 23.0
```
docker pull eloebel/glacier-front-extraction:latest
```

satellite scene in folder input (path has to be set)

```
docker run --volume=/home/INPUT_IMAGES:/input --env glacier=zachariae_isstrom eloebel/glacier-front-extraction:latest
```

for example coordinates (glacier front (windo 15x15 km around), decimal degrees -180 bis 180

```
docker run --volume=/home/INPUT_IMAGES:/input --env glacier=custom --env lon=59.98 --env lat=-64.37 eloebel/glacier-front-extraction:latest
```

prediction will be a separate folder in input conatining shp and overview and tif mask
### Option 2: Singularity
tested for version 3.8
does not require root
```
singularity pull docker://eloebel/glacier-front-extraction:latest
```
```
singularity run --bind /home/INPUT_IMAGES:/input --bind /home/DATA:/data --env glacier=zachariae_isstrom glacier-front-extraction_latest.sif
```
```
singularity run --bind /home/INPUT_IMAGES:/input --bind /home/DATA:/data --env glacier=custom --env lon=-28.57 --env lat=71.91 glacier-front-extraction_latest.sif
```
data folder with pre processid input can be deleted. if not it will pre delineated on subsequent container runs
### Option 3: Use scripts provided in this repositiry
```
conda create --name <env_name> --file requirements.txt
```

```
python GLACIER_FRONT_EXTRACTION.py daugaard_jensen
```

```
python GLACIER_FRONT_EXTRACTION.py custom -28.57 71.91
```

Download model weights and use scripts provided in this repositiry

## Example
This is the ANN applied to satellite image of Daugaard Jensen Glacer in east Greenland. For quantifying the change in calving front position you can use our implementation of the rectilinear box method.
![loebel_calving_fronts](https://user-images.githubusercontent.com/68990782/225654755-5d85399f-11a8-40a3-b217-dfc1cc002a63.gif)

## Contact
**Erik Loebel**  
TU Dresden | Geodetic Earth System Research   
[tu-dresden.de/geo/ipg/gef](https://tu-dresden.de/bu/umwelt/geo/ipg/gef)  
[erik.loebel@tu-dresden.de](mailto:erik.Loebel@tu-dresden.de)  
[@ErikLoebel](https://twitter.com/erikloebel)  
