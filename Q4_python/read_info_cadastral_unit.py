import processing

import time
start_time = time.time()

# ------------------------------------------------------------------------------
#                              path of the input 
# ------------------------------------------------------------------------------
# import the shape file 
path = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/info/"
cadastre_file = path+"Cuneo_shapefile/all 2021.shp"


# consortia layer and plot
cadastre_layer = QgsVectorLayer(cadastre_file, "all", "ogr")
QgsProject.instance().addMapLayer(cadastre_layer)

idx = cadastre_layer.fields().indexOf('cens_liv4')
values = cadastre_layer.uniqueValues(idx)
                
print(values)
# ------------------------------------------------------------------------------
#                               print the results
# ------------------------------------------------------------------------------ 
print('************************')
print('Time duration')
print(" %s seconds " % (time.time() - start_time))



