import processing
import tool_function 

import time
start_time = time.time()

# ------------------------------------------------------------------------------
#                              path of the input 
# ------------------------------------------------------------------------------
# import the shape file 
path = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/Georeference/"
cadastre = path+"Cuneo_shapefile/all 2021.shp"
polygone = "Test_polygons.shp"


# ------------------------------------------------------------------------------
#                       get the list of crops inside the polygone
# ------------------------------------------------------------------------------
list_crop = get_list_crops(path, polygone, cadastre)


# ------------------------------------------------------------------------------
#                               centroids of polygon
# ------------------------------------------------------------------------------ 
centroids_output = path + "centroids.shp"
centroids_output = centroids(path+input, centroids_output)


# ------------------------------------------------------------------------------
#                               water need for each crop
# ------------------------------------------------------------------------------ 
dict_crop_wn_medi, dict_crop_wn_sup = get_all_crops_needs( list_crop, centroids_output)
                
                
# ------------------------------------------------------------------------------
#                               print the results
# ------------------------------------------------------------------------------ 
print('************************')
print('Time duration')
print(" %s seconds " % (time.time() - start_time))



