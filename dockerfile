# syntax=docker/dockerfile:1
FROM tensorflow/tensorflow

WORKDIR /scripts
WORKDIR /data
VOLUME /input

### install app dependencies
RUN apt-get update && apt-get install -y wget && apt-get install -y gdal-bin
RUN pip install tifffile && pip install matplotlib && pip install tqdm && pip install pyshp

### copying files
COPY GLACIER_FRONT_EXTRACTION.py /scripts
COPY pre-processing.sct /scripts
COPY frontlagen_center_coord.txt /scripts
COPY spectral_pre-processing.py /scripts
COPY predict_calving_front.py /scripts
COPY mask_coastline.sct /scripts
COPY vectorize_prediction.sct /scripts
COPY model_weights /scripts
COPY merge_prediction.py /scripts
COPY gdal_operations_humboldt.sct /scripts
COPY gdal_operations_nioghalvfjerdsbrae.sct /scripts
COPY gdal_operations_zachariae.sct /scripts
ADD Frontpolygone /scripts/Frontpolygone

### run script
ENV glacier no_glacier
CMD python /scripts/GLACIER_FRONT_EXTRACTION.py $glacier
