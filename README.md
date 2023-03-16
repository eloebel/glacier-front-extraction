# Automated calving front delineation from multispectral satellite imagery using deep learning
We provide a containerized implementation of the presented processing system. The software automatically extracts calving front positions from Landsat-8 or Landsat-9 Level-1 data archives for glacier used within this study or at user-defined coordinates. This enables the analysis of glaciers that are outside our reference dataset or beyond the temporal frame of our study.
## Usage
We provide three options for using this software. We recommend using the containerized implementation via Docker (option 1) or Singularity (option 2).
### Option 1: Docker
```
docker pull eloebel/glacier-front-extraction:latest
```
```
sudo docker run --volume=/home/INPUT_IMAGES:/input --env glacier=zachariae_isstrom eloebel/glacier-front-extraction:latest
```
### Option 2: Singularity
```
singularity pull docker://eloebel/glacier-front-extraction:latest
```
```
singularity run --bind /home/INPUT_IMAGES:/input --bind /home/DATA:/data --env glacier=zachariae_isstrom glacier-front-extraction_latest.sif
```
### Option 3: Download weights and use scripts provided in this repositiry
Interested in datasets -> manual here -> autoamted big set here  
box method here


![git_examples](https://user-images.githubusercontent.com/68990782/225638176-8bec927c-b9b7-4fc9-87c6-aa0af7f3ac77.png)


## Contact
**Erik Loebel**  
TU Dresden | Geodetic Earth System Research   
[tu-dresden.de/geo/ipg/gef](https://tu-dresden.de/bu/umwelt/geo/ipg/gef)  
[erik.loebel@tu-dresden.de](mailto:erik.Loebel@tu-dresden.de)  
[@ErikLoebel](https://twitter.com/erikloebel)  
