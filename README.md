# Automated calving front delineation from multispectral satellite imagery using deep learning

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://zenodo.org/badge/330633305.svg)](https://doi.org/10.5281/zenodo.7755773)

This software automatically delineates calving front positions from Landsat-8 and Landsat-9 Level-1 data archives. It processes multispectral imagery using a specialized artificial neural network (ANN). In particular, it uses a convolutional neural network of the U-Net architecture to semantically segment images into a glacier/land and water class. The glacier calving front, which is described by the boundary between these two classes, is then extracted by vectorizing and masking the model prediction. The figure below gives a broad overview of the processing workflow.

![workflow_v5](https://user-images.githubusercontent.com/68990782/225638941-61c5c4ca-3319-4894-92aa-f81d853dbf15.png)

The model is trained using manually delineated calving front position from 23 Greenland and 12 Antarctic Peninsula outlet glaciers. We evaluated the performance of this model using three independent test datasets, including glaciers in Svalbard and in Patagonia. The quality of the automatically extracted calving fronts is comparable to that of manually delineated calving fronts. The processing system and its validation are described in detail in [this article](https://tc.copernicus.org/articles/18/3315/2024/). Details of the performance specifically for the Antarctic Peninsula are also published [here](https://essd.copernicus.org/articles/17/65/2025/essd-17-65-2025.html).

## Usage
The recommended option to use this software is to download the ANN weights and use the routines in this repository (option 1). The scripts in this repository are kept up to date to ensure compatibility with the latest conventions for Landsat imagery (currently Collection 2). It is also possible to use a containerized implementation via Docker (option 2) or Singularity (option 3). These containerized versions are based on an older version of the deep learning model (which delivers inferior performance), and are no longer maintained.

### Option 1: Use scripts provided in this repository
Clone the repository and install all required python packages. You can use the requirements.txt with conda:
```
conda create --name <env_name> --file requirements.txt
```
Download the ANN model weights from the latest release and unpack them into the main repository folder. Place the Landsat archives to be processed in the `input` folder (see placeholder). This software is coded for bulk processing. The input folder can be filled with an unlimited number of Landsat archieves.

```
python GLACIER_FRONT_EXTRACTION.py daugaard_jensen
```
Glaciers outside the reference dataset can also be processed. To do this, set the glacier name to `custom` and define `lon` and `lat` coordinates (decimal degrees) as environment variables. The processing window is approximately 15 km by 15 km, centered on these defined coordinates. Example for a calving front extraction for 28.57°W and 71.91°N:
```
python GLACIER_FRONT_EXTRACTION.py custom -28.57 71.91
```
The ANN calving front prediction is stored in a separate folder within the defined input directory. The prediction contains the coastline, the calving front (LineString Shapefile), the prediction mask (geoTiff) and an overview figure.

### Option 2: Docker
The docker container contains the code, model weights and all requirements to run the processing system (tested for Docker version 23.0). Download the container by running:
```
docker pull eloebel/glacier-front-extraction:latest
```
Place the Landsat archives to be processed in an input folder. Run the container and define the path of this input folder and set the glacier name as an environment variable.

```
docker run --volume=/home/INPUT_IMAGES:/input --env glacier=daugaard_jensen eloebel/glacier-front-extraction:latest
```
Glaciers outside the reference dataset can also be processed. To do this, set the glacier name to `custom` and define `lon` and `lat` coordinates (decimal degrees) as environment variables. The processing window is approximately 15 km by 15 km, centered on these defined coordinates. Example for a calving front extraction for 28.57°W and 71.91°N:
```
docker run --volume=/home/INPUT_IMAGES:/input --env glacier=custom --env lon=-28.57 --env lat=71.91 eloebel/glacier-front-extraction:latest
```
The ANN calving front prediction is stored in a separate folder within the defined input directory. The prediction contains the coastline, the calving front (LineString Shapefile), the prediction mask (geoTiff) and an overview figure.

### Option 3: Singularity
Docker contains can also be run with Singularity (tested for Singularity version 3.8). Download the container and convert into a Singularity image by running:
```
singularity pull docker://eloebel/glacier-front-extraction:latest
```
Place the Landsat archives you want to process in an input folder. Run the container and bind the path to this input folder. In addition, you have to bind a data folder which is needed for storing temporary data. The glacier name is defined using an environment variable.

```
singularity run --bind /home/INPUT_IMAGES:/input --bind /home/DATA:/data --env glacier=daugaard_jesen glacier-front-extraction_latest.sif
```
Glaciers outside the reference dataset can also be processed. To do this, set the glacier name to `custom` and define `lon` and `lat` coordinates (decimal degrees) as environment variables. The processing window is approximately 15 km by 15 km, centered on these defined coordinates. Example for a calving front extraction for 28.57°W and 71.91°N:
```
singularity run --bind /home/INPUT_IMAGES:/input --bind /home/DATA:/data --env glacier=custom --env lon=-28.57 --env lat=71.91 glacier-front-extraction_latest.sif
```
The ANN calving front prediction is stored in a separate folder within the defined input directory. The prediction contains the coastline, the calving front (LineString Shapefile), the prediction mask (geoTiff) and an overview figure. The data folder containing temporary data (especially the pre-processed satellite images) can be deleted. Otherwise, the ANN is applied to the data in subsequent container runs.

## Example
This is an example of our software applied to Landsat images of the Daugaard Jensen Glacier in East Greenland. To quantify the change in the position of the calving front, you can use [our implementation of the rectilinear box method](https://github.com/eloebel/rectilinear-box-method).

![loebel_calving_fronts](https://user-images.githubusercontent.com/68990782/225654755-5d85399f-11a8-40a3-b217-dfc1cc002a63.gif)


## Greenland glaciers
The following Greenland glaciers can be selected directly from the environment variable. For these glaciers, the processing system extracts not only the entire coastline but also the masked glacier front. Glaciers outside the reference dataset can also be processed. To do this, set the glacier name to custom and define the `lon` and `lat` coordinates (decimal degrees).
| Glacier      | environment variable |
| ----------- | ----------- |
| Kangiata Nunaata Sermia      | kangiata_nunaata_sermia       |
| Helheim Glacier   | helheim        |
| Kangerdlussuaq Glacier   | kangerdlugssuaq        |
| Jakobshavn Isbræ   | jakobshavn_isbrae        |
| Store Glacier   | store        |
| Rink Isbræ   | rinks_isbrae        |
| Daugaard Jensen Glacier   | daugaard_jensen        |
| Ingia Isbræ   | ingia_isbrae        |
| Upernavik Isstrøm   | upernavik_isstrom_north        |
| Waltershausen Glacier   | waltershausen_glacier        |
| Hayes Glacier   | hayes        |
| Sverdrup Glacier   | sverdrup        |
| Kong Oscar Glacier   | kong_oscar        |
| Døcker Smith Glacier   | docker_smith        |
| Harald Molke Bræ   | harald_moltke_brae        |
| Tracy Glacier   | tracy_gletscher        |
| Humboldt Glacier   | humboldt        |
| Zachariae Isstrøm   | zachariae_isstrom        |
| Nioghalvfjerdsbræ   | nioghalvfjerdsbrae        |
| Hagen Bræ   | hagen_brae        |
| Academy Glacier   | academy        |
| Ryder Glacier   | ryder_glacier        |


## Antarctic Peninsula glaciers
The following Antarctic Peninsula glaciers can be selected directly from the environment variable. Glaciers outside the reference dataset can also be processed. To do this, set the glacier name to custom and define the `lon` and `lat` coordinates (decimal degrees).
| Glacier      | environment variable |
| ----------- | ----------- |
| Boydell Glacier      | boydell       |
| Drygalski Glacier   | drygalski        |
| Edgeworth Glacier   | edgeworth        |
| Fleming Glacier   | fleming        |
| Prospect Glacier  | prospect       |
| Hariot Glacier   | hariot        |
| Murphy Wilkinson Glacier    | murphy_wilkinson        |
| Widdowson Glacier   | widdowson        |
| Hugi Glacier   | hugi        |
| Birley Glacier   | birley        |
| Bleriot Glacier   | bleriot        |
| Crane Glacier   | crane        |
| Trooz Glacier   | trooz        |
| Hektoria-Green-Evans Glacier system   | hektoria-green-evans      |
| Jorum Glacier   | jorum       |
| Cayley Glacier   | cayley       |
| Carlson Glacier   | carlson        |
| Clarke Glacier   | clarke        |
| Remus Glacier  | remus        |
| Swithinbank Glacier   | swithinbank        |
| Valot Glacier   | valot       |
| Avsyuk Glacier   | avsyuk        |
| Peter Glacier   | peter       |
| McCance Glacier   | mccance       |
| Hopkins Glacier   | hopkins       |
| Erskine Glacier   | erskine       |
| Keith Glacier   | keith       |
| Otlet Glacier   | otlet       |
| Cadmand and Funk Glacier   | cadman_funk       |
| Renard-Krebs Glacier   | renard_krebs       |
| Temple Glacier   | temple       |
| Malorad Glacier   | malorad       |
| Pyke Glacier   | pyke      |
| Darvari-Boryana-Desudava Glacier system   | darvari-boryana-desudava       |
| Akaga-Sinion Glacier system,   | akaga-sinion-zaychar       |
## Citation
If you find our software helpful and use it in your research, please use the following BibTeX entry.
````
@Article{loebel2024,
AUTHOR = {Loebel, E. and Scheinert, M. and Horwath, M. and Humbert, A. and Sohn, J. and Heidler, K. and Liebezeit, C. and Zhu, X. X.},
TITLE = {Calving front monitoring at a subseasonal resolution: a deep learning application for Greenland glaciers},
JOURNAL = {The Cryosphere},
VOLUME = {18},
YEAR = {2024},
NUMBER = {7},
PAGES = {3315--3332},
URL = {https://tc.copernicus.org/articles/18/3315/2024/},
DOI = {10.5194/tc-18-3315-2024}
}
````

## Contact
**Erik Loebel**  
TU Dresden | Geodetic Earth System Research   
[tu-dresden.de/geo/ipg/gef](https://tu-dresden.de/bu/umwelt/geo/ipg/gef)  
[erik.loebel@tu-dresden.de](mailto:erik.Loebel@tu-dresden.de)  
