# Automated calving front delineation from multispectral satellite imagery using deep learning

We provide a containerized implementation of the presented processing system. The software automatically extracts calving front positions from Landsat-8 or Landsat-9 Level-1 data archives for glacier used within this study or at user-defined coordinates. This enables the analysis of glaciers that are outside our reference dataset or beyond the temporal frame of our study.
![workflow_v5](https://user-images.githubusercontent.com/68990782/225638941-61c5c4ca-3319-4894-92aa-f81d853dbf15.png)


## Usage
We provide three options for using this software. We recommend using the containerized implementation via Docker (Option 1) or Singularity (Option 2).
### Option 1: Docker
```
docker pull eloebel/glacier-front-extraction:latest
```
```
sudo docker run --volume=/home/INPUT_IMAGES:/input --env glacier=zachariae_isstrom eloebel/glacier-front-extraction:latest
```
```
sudo docker run --volume=/home/INPUT_IMAGES:/input --env glacier=custom --lon=59.98 --lat=-64.37 eloebel/glacier-front-extraction:latest
```
### Option 2: Singularity
```
singularity pull docker://eloebel/glacier-front-extraction:latest
```
```
singularity run --bind /home/INPUT_IMAGES:/input --bind /home/DATA:/data --env glacier=zachariae_isstrom glacier-front-extraction_latest.sif
```
### Option 3: Use scripts provided in this repositiry
Download model weights and use scripts provided in this repositiry


![loebel_calving_fronts](https://user-images.githubusercontent.com/68990782/225654755-5d85399f-11a8-40a3-b217-dfc1cc002a63.gif)


## Contact
**Erik Loebel**  
TU Dresden | Geodetic Earth System Research   
[tu-dresden.de/geo/ipg/gef](https://tu-dresden.de/bu/umwelt/geo/ipg/gef)  
[erik.loebel@tu-dresden.de](mailto:erik.Loebel@tu-dresden.de)  
[@ErikLoebel](https://twitter.com/erikloebel)  
