# Automated extraction of calving front locations from multi-spectral satellite imagery using deep learning
The calving of tidewater glaciers has a strong impact on the stresses of outlet glaciers and their
discharge. However, it is still underrepresented in current ice-sheet models incorporating the
dynamics of marine-terminating glaciers. This has an impact on simulation results when projecting
future sea-level contributions of the Greenland ice sheet. The increasing availability and quality of
remote sensing imagery enable us to realize a continuous and precise mapping of relevant
parameters such as calving front locations. However, the huge amount of data also accentuates
the necessity for intelligent analysis strategies.
In this contribution, we apply an automated workflow to extract calving front positions from multi-
spectral Landsat-8 imagery utilizing deep learning. The core of the proposed workflow comprises a
convolutional neural network (CNN) for image segmentation exploiting the full range of Landsat-8
multi-spectral capabilities, a statistical textural feature analysis performed on the high-resolution
panchromatic band as well as topography model data. The proposed method is evaluated by an
independent set of diverse test images as well as by comparing with already available ESA-CCI,
MEaSUREs and PROMICE data products. With an estimated prediction error of fewer than two
pixels (which equals a spatial resolution of 60 m), automatically extracted calving front locations
show very small or even non-distinguishable differences to manually delineated locations. The
importance of multi-spectral, textural and topographic features used as input for the CNN is
estimated by a permute-and-relearn approach emphasizing their benefit, especially in challenging
ice-melange, cloud, and illumination conditions. Jointly with the proposed methodology we
present an exceedingly dense dataset for 20 of the most important Greenlandic outlet glaciers for
the period from 2013 to 2021.
Eventually, the derived calving front positions are incorporated into the Ice Sheet and Sea-Level
System Model (ISSM). For this, we engage a level set method. This method allows deriving a
continuous function in time and space from discrete information at satellite acquisition time steps.
As the satellite data is mainly available for fast-flowing outlet glaciers, we use simulated front
positions for all remaining ice margins. An alpha-shape method seamlessly links the temporal
changing calving fronts to the Greenlandic ice sheet.
