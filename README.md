# Automated calving front delineation from multispectral satellite imagery using deep learning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This software automatically delineates calving front positions from Landsat-8 and Landsat-9 Level-1 data archives. It processes multispectral imagery using a specialized artificial neural network (ANN). In particular, it uses a convolutional neural network of the U-Net architecture to semantically segment images into a glacier/land and water class. The glacier calving front, which is described by the boundary between these two classes, is then extracted by vectorizing and masking the model prediction. The figure below gives a broad overview of the processing workflow.

![workflow_v5](https://user-images.githubusercontent.com/68990782/225638941-61c5c4ca-3319-4894-92aa-f81d853dbf15.png)

Model is trained using manually delineated calving front position from 19 Greenland glaciers. We evaluated the performance of this model using three independent test datasets, including glaciers in Svalbard, at the Antarctic Peninsula and in Patagonia. The quality of the automatically extracted calving fronts is comparable to that of manually delineated calving fronts. The processing system and its validation are described in detail in [this article](https://doi.org/10.1109/TGRS.2022.3208454).

## Usage
We offer three options for using this software. We recommend using the containerised implementation via Docker (option 1) or Singularity (option 2). It is also possible to download the ANN weights and use the routines in this repository (option 3).
### Option 1: Docker
The docker container contains the code, model weights and all requirements to run the processing system (tested for Docker verison 23.0). Download the container by running:
```
docker pull eloebel/glacier-front-extraction:latest
```
Place the Landsat archives to be processed in an input folder. Run the container and define the path of this input folder and set the glacier name as an environment variable.

```
docker run --volume=/home/INPUT_IMAGES:/input --env glacier=daugaard_jensen eloebel/glacier-front-extraction:latest
```
Glaciers outside the reference dataset can also be processed. To do this, set the glacier name to `custom` and define `lon` and `lat` coordinates (decimal degrees) as environment variables. The processing window is approximately 15 km by 15 km, centred on these defined coordinates. Example for a calving front extraction for 28.57°W and 71.91°N:
```
docker run --volume=/home/INPUT_IMAGES:/input --env glacier=custom --env lon=-28.57 --env lat=71.91 eloebel/glacier-front-extraction:latest
```
The ANN calving front prediction will be saved in a separete folder inside the defined input directory. The prediction containes the coastline, the calving front (LineString Shapefile), the prediction mask (geoTiff) and an overview figure.

### Option 2: Singularity
Docker containes can also be run with Singularity (tested for Singularity verison 3.8). Download the container and convert into a Singularity image by running:
```
singularity pull docker://eloebel/glacier-front-extraction:latest
```
Place the Landsat archives you want to process in an input folder. Run the container and bind the path to this input folder. In addition you have to bind a data folder which is needed for storing temporary data. The glacier name is defined using an environment variable.

```
singularity run --bind /home/INPUT_IMAGES:/input --bind /home/DATA:/data --env glacier=daugaard_jesen glacier-front-extraction_latest.sif
```
Glaciers outside the reference dataset can also be processed. To do this, set the glacier name to `custom` and define `lon` and `lat` coordinates (decimal degrees) as environment variables. The processing window is approximately 15 km by 15 km, centred on these defined coordinates. Example for a calving front extraction for 28.57°W and 71.91°N:
```
singularity run --bind /home/INPUT_IMAGES:/input --bind /home/DATA:/data --env glacier=custom --env lon=-28.57 --env lat=71.91 glacier-front-extraction_latest.sif
```
The ANN calving front prediction is stored in a separate folder within the defined input directory. The prediction contains the coastline, the calving front (LineString Shapefile), the prediction mask (geoTiff) and an overview figure. The data folder containing temporary data (especially the pre-processed satellite images) can be deleted. Otherwise, the ANN is applied to the data in subsequent container runs.
### Option 3: Use scripts provided in this repositiry
Clone the repository and install all required python packages. You can use the requirements.txt with conda:
```
conda create --name <env_name> --file requirements.txt
```
Download the ANN model weights and move them to the main repository folder. Place the Landsat archives to be processed in the `input` folder (see placeholder).

```
python GLACIER_FRONT_EXTRACTION.py daugaard_jensen
```
Glaciers outside the reference dataset can also be processed. To do this, set the glacier name to `custom` and define `lon` and `lat` coordinates (decimal degrees) as environment variables. The processing window is approximately 15 km by 15 km, centred on these defined coordinates. Example for a calving front extraction for 28.57°W and 71.91°N:
```
python GLACIER_FRONT_EXTRACTION.py custom -28.57 71.91
```
The ANN calving front prediction will be saved in a separete folder inside the defined input directory. The prediction containes the coastline, the calving front (LineString Shapefile), the prediction mask (geoTiff) and an overview figure.

## Example
This is an example of our software applied to Landsat imagery of glacier Daugaard Jensen Glacier in east Greenland.
To quantify the change in the position of the calving front, you can use [our implementation of the rectilinear box method](https://github.com/eloebel/rectilinear-box-method).

![loebel_calving_fronts](https://user-images.githubusercontent.com/68990782/225654755-5d85399f-11a8-40a3-b217-dfc1cc002a63.gif)


## Greenland glaciers
The following Greenland glaciers can be selected directly from the environment variable. For these glaciers, the processing system extracts not only the entire coastline but also the masked glacier front. Glaciers outside the reference dataset can also be processed. To do this, set the glacier name to custom and define the `lon` and `lat` coordinates (decimal degrees).
| Glacier      | environment variable |
| ----------- | ----------- |
| Header      | Title       |
| Paragraph   | Text        |

## Contact
**Erik Loebel**  
TU Dresden | Geodetic Earth System Research   
[tu-dresden.de/geo/ipg/gef](https://tu-dresden.de/bu/umwelt/geo/ipg/gef)  
[erik.loebel@tu-dresden.de](mailto:erik.Loebel@tu-dresden.de)  
[@ErikLoebel](https://twitter.com/erikloebel)  
