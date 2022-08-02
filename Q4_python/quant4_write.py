print(before lauching the program, you have to lauch, get_consortia_info_v2.py, get_water_need.py, Tool_function.py,coltura_reference.py, excel_writting.py)
# ==============================================================================
#                                  Input of the program
# ==============================================================================

# --------------------------------- 
#          Result folder
# ---------------------------------
result_folder = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/Results/"             #"""  write """

# ---------------------------------
#            Consortia
# --------------------------------- 
consortia_path = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/consortia/"     #"""  write """
consortia_name_file = "CI_CORVA_SINISTRA.shp"                                          #"""  write """
consortia_file = consortia_path + consortia_name_file

# consortia layer and plot
consortia_layer = QgsVectorLayer(consortia_file, "Consortia", "ogr")
QgsProject.instance().addMapLayer(consortia_layer)

# max_area 
consortia_max_area_authorized = 10000  #in Ha                                            """  write """
is_area_valid(consortia_layer, consortia_max_area_authorized)

# get the name of the consortia
idx = consortia_layer.fields().indexOf('DENOMINAZI')
list_consortia = list(consortia_layer.uniqueValues(idx))


# ---------------------------------
#              Cadastre
# ---------------------------------
cadastre_path = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/Cuneo_shapefile/" #"""  write """
cadastre_name_file =  "all 2021.shp"                                                    #"""  write """
cadastre_file = cadastre_path + cadastre_name_file


# ---------------------------------
#           Permeability
# ---------------------------------
permeability_path = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/permeability/" #""""  write """
permeability_name_file = "capacita_uso_suoli_con_drenaggio.shp"                          #"""  write """
permeability_file = permeability_path + permeability_name_file


# ---------------------------------
#         Water need folder
# ---------------------------------
raster_folder = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/Georeference/"     #"""  write """


# ---------------------------------
#             Excel file
# ---------------------------------
name = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/Quant4/quant4_vers_4_2_xls_ORIGINALE.xls" #"""  write """
Inizio = '01/04'                                                                                 #"""  write """
Terminea = '30/09'                                                                               #"""  write """
Ex_write = Excel_write(name,  
                       list_consortia[0],
                       6.064,
                       Inizio,
                       Terminea)

# ---------------------------------
#            Type of canali
# ---------------------------------
# collectiva
canali_terra = 100                                                                               #"""  write """
canali_rivestiti_simili = 0                                                                      #"""  write """
condotte = 0                                                                                     #"""  write """
Ex_write.add_composizione_irrigua_collectiva(canali_terra,
                                             canali_rivestiti_simili,
                                             condotte)
# aziendale 
canali_terra_az = 100                                                                            #"""  write """  
canali_rivestiti_simili_az = 0                                                                   #"""  write """  
condotte_az = 0                                                                                  #"""  write """
Ex_write.add_composizione_irrigua_aziendale(canali_terra_az,
                                             canali_rivestiti_simili_az,
                                             condotte_az)
                                             

# ---------------------------------
#     Coltura reference data base 
# ---------------------------------
name = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/Quant4/Coltura_reference.xlsx"           #"""  write """
Excel_coltura = Excel_reference_coltura(name)


# ==============================================================================
#                                  Create the usefull the file 
# ==============================================================================

# ------------------- 
#     Cadastre
# --------------------
cadastre_in_consortia =  "cadastre_in_consortia.shp"
output_cadastre = intersection(consortia_file, 
                               cadastre_file,
                               result_folder + cadastre_in_consortia)
                               
# plot the layer                                 
cadastre_layer = QgsVectorLayer(output_cadastre, "Cadastre", "ogr")
QgsProject.instance().addMapLayer(cadastre_layer)

# time 
print('************************')
print('Cadastre file created ')
print(" %s seconds " % (time.time() - start_time))

# ------------------- 
#     Permeability
# --------------------
permeability_in_consortia =  "permeability_in_consortia.shp"
output_permeability = intersection(consortia_file,
                                   permeability_file, 
                                   result_folder + permeability_in_consortia)
  
# plot the layer  
permea_layer = QgsVectorLayer(output_permeability, "Permeability", "ogr")
QgsProject.instance().addMapLayer(permea_layer)

# calculate the ratio of type of soil on area of the consortia
name_field = "Ratio_%"
expression = '$area/"AREA_HA"/10000'
add_field(permea_layer, name_field, expression)

# time 
print('************************')
print('Permeability file created ')
print(" %s seconds " % (time.time() - start_time))


# ------------------- 
#     Centroids
# --------------------
centroids_name_file =  "centroids.shp"
centroids_output = centroids( consortia_file, 
                              False, 
                              result_folder + centroids_name_file)

# plot the layer
centroids_layer = QgsVectorLayer(centroids_output, "Centroids", "ogr")
QgsProject.instance().addMapLayer(centroids_layer)


# ==============================================================================
#                                 Get  info  
# ==============================================================================
consortia = list_consortia[0]
# ------------------- 
#    Consortia info
# --------------------
dict_coltura, dict_perma  = collect_information_consortium(result_folder,
                                                           cadastre_layer,
                                                           permea_layer,
                                                           list_consortia)

# ------------------- 
#    monthly water need 
# --------------------
list_crop = get_list_crops(result_folder , 
                           consortia_file, 
                           result_folder + cadastre_in_consortia)


# water need for each crop 
dict_Fabbisogni_50, dict_Fabbisogni_20, list_non_reference_crop = get_all_crops_needs(list_crop, 
                                                                                      centroids_output,
                                                                                      raster_folder)

print('************************')
print('Collect the info')
print(" %s seconds " % (time.time() - start_time))

# ==============================================================================
#                               Write information  
# ==============================================================================

dict_reference_coltura = Excel_coltura.collect_all_information(list_non_reference_crop)
# ------------------- 
#      Culture
# --------------------
for coltura in dict_reference_coltura.keys():
    Ex_write.add_new_coltura(coltura, dict_reference_coltura[coltura])

# ------------------- 
#      Culture
# --------------------
Ex_write.add_all_coltura_irrigate(dict_coltura[consortia],list(dict_reference_coltura.keys()))

# ------------------- 
#    Permeability
# --------------------
Ex_write.add_permeability_matrix(dict_perma[consortia])


# ------------------- 
#    Water need
# --------------------
Ex_write.add_fabbisogni_netti_medi(dict_Fabbisogni_50)
Ex_write.add_fabbisogni_netti_20(dict_Fabbisogni_20)

print('************************')
print('Info written')
print(" %s seconds " % (time.time() - start_time))
# ==============================================================================
#                               New coltura  
# ==============================================================================


# ==============================================================================
#                                 Save the results  
# ==============================================================================
Ex_write.workbook.save(Ex_write.output_name)
print('************************')
print('End programm')
print(" %s seconds " % (time.time() - start_time))




