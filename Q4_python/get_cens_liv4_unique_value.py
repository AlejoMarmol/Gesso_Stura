# ==============================================================================
#                                  Input of the program
# ==============================================================================

# ---------------------------------
#            Consortia
# --------------------------------- 
consortia_path = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/consortia/"     #"""  write """
consortia_name_file = "AREA_BORCA_1.shp"                                               #"""  write """
consortia_file = consortia_path + consortia_name_file

# consortia layer and plot
consortia_layer = QgsVectorLayer(consortia_file, "Consortia", "ogr")
QgsProject.instance().addMapLayer(consortia_layer)

# ---------------------------------
#              Cadastre
# ---------------------------------
cadastre_path = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/Cuneo_shapefile/" #"""  write """
cadastre_name_file =  "all 2021.shp"                                                    #"""  write """
cadastre_file = cadastre_path + cadastre_name_file


# ==============================================================================
#                              iNTERSECTION Consortia cadastre 
# ==============================================================================
# ------------------------
#   intersection function  
# -------------------------
def intersection(input, overlay, ouput):
    """
    realize an intersection between two file 
    """
    # parameters 
    params = {
     'INPUT': input,
     'OVERLAY': overlay,
     'OUTPUT': ouput}
     
    # outputdict : {'OUPUT': file path'}     
    outputdict = processing.run('qgis:intersection', params)
    return(outputdict['OUTPUT'])
    
# ------------------------
#   intersection   
# -------------------------
cadastre_in_consortia =  "cadastre_in_consortia.shp"
output_cadastre = intersection(consortia_file, 
                               cadastre_file,
                               result_folder + cadastre_in_consortia)


# ==============================================================================
#                              Output and plot  
# ==============================================================================                               
# plot the layer                                 
cadastre_layer = QgsVectorLayer(output_cadastre, "Cadastre", "ogr")
QgsProject.instance().addMapLayer(cadastre_layer)

# get the list of crops
idx = cadastre_layer.fields().indexOf('cens_liv4')
values = cadastre_layer.uniqueValues(idx)
                
print(values)