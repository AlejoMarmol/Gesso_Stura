from qgis.core import *
import os

import time
start_time = time.time()

# directory of the shape file
directory = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/Georeference/Cuneo_shapefile/"

# Get the list of input files
fileList = os.listdir(directory)

# Copy the features from all the files in a new list
fileshp = []
name_cities = {}
for file in fileList:
    if file.endswith('.shp'):
        fileshp.append(directory + file)
        name_file = file.split('_')
        if name_file [0] not in name_cities.keys() :
            name_cities[name_file [0]] = [directory +file]
        else :
            name_cities[name_file [0]].append(directory +file)
            


layer_cities =[]
for municipality in name_cities.keys() :
    municipality_ouput = directory + municipality + " 2021.shp"
    print(municipality)
    if len(name_cities[municipality])> 1 and municipality not in ['Limone Piemonte']:
        param_merge = {
            'LAYERS': name_cities[municipality],
            'CRS':QgsCoordinateReferenceSystem('EPSG:32632'),
            'OUTPUT' : municipality_ouput
            }
        processing.run("native:mergevectorlayers",param_merge)

        layer_cities.append(directory + municipality + " 2021.shp")


# create one file 
param_merge = {
            'LAYERS': layer_cities,
            'CRS':QgsCoordinateReferenceSystem('EPSG:32632'),
            'OUTPUT' : directory + 'all 2021.shp'
            }
processing.run("native:mergevectorlayers",param_merge)


# ------------------------------------------------------------------------------
#                               print the results
# ------------------------------------------------------------------------------ 
print('Time duration')
print(" %s seconds " % (time.time() - start_time))