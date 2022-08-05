print('before lauching the program, you have to lauch :')
print(' - get_consortia_info_v2.py')
print(' - get_water_need.py')
print(' - Tool_function.py')
print(' - coltura_reference.py')
print(' - excel_writting.py')
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
consortia_name_file = "AREA_BORCA_1.shp"                                               #"""  write """
consortia_file = consortia_path + consortia_name_file

id_field_consortia = 'DENOMINAZI'                                                      #"""  write """

# consortia layer and plot
consortia_layer = QgsVectorLayer(consortia_file, "Consortia", "ogr")
QgsProject.instance().addMapLayer(consortia_layer)

# max_area 
consortia_max_area_authorized = 10000  #in Ha                                            """  write """
is_area_valid(consortia_layer, consortia_max_area_authorized)

# get the name of the consortia
idx = consortia_layer.fields().indexOf(id_field_consortia)
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
name_output = result_folder + "quant4_vers_4_2_"+ consortia_name_file
Inizio = '01/04'                                                                                 #"""  write """
Terminea = '30/09'                                                                               #"""  write """
numero_consortia = 6.064                                                                               #"""  write """

Ex_write = Excel_write(name,  
                       name_output,
                       str(list_consortia[0]),
                       numero_consortia,
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
name = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/Quant4/Coltura_data_base.xlsx"           #"""  write """
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
                               
# the layer                                 
cadastre_layer = QgsVectorLayer(output_cadastre, "Cadastre", "ogr")

# calculate the area of each particella 
name_field = 'Area_part'
expression = '$area/10000'
add_field(cadastre_layer, name_field, expression)

# plot the layer 
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
  
# the layer  
permea_layer = QgsVectorLayer(output_permeability, "Permeability", "ogr")

# calculate the ratio of type of soil on area of the consortia
name_field = "Ratio_%"
expression = '$area/"AREA"/10000'
add_field(permea_layer, name_field, expression)

# plot the layer 
QgsProject.instance().addMapLayer(permea_layer)
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
                                                           list_consortia,
                                                           id_field_consortia)

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
# order the dict_coltura 
dict_coltura = dict_coltura[consortia]
list_new_reference_type_crop = list(dict_reference_coltura.keys())
list_type_crop = dict_Fabbisogni_50.keys()

dict_consortia_coltura = order_dict_coltura(dict_coltura,
                                            list_new_reference_type_crop, 
                                            list_type_crop)

Ex_write.add_all_coltura_irrigate(dict_consortia_coltura,list_new_reference_type_crop)

# ------------------- 
#    Permeability
# --------------------
Ex_write.add_permeability_matrix(dict_perma[consortia])


# ------------------- 
#    Water need
# --------------------
for coltura in dict_Fabbisogni_50.keys():
    Ex_write.add_fabbisogni_netti_medi(coltura, dict_Fabbisogni_50[coltura])
    Ex_write.add_fabbisogni_netti_20(  coltura, dict_Fabbisogni_20[coltura])

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


print('************************')
print(' As in information if you are questionning about the crop you have decided to negligated and reference then into : list_non_desired_crop, in coltura.reference.py, you can stil look at the value of the superficie covered by each crop.')
print('This information is store in dict_coltura ( key = crop, value = superficie irrigate), you can print it by taping :')
print('print(dict_coltura)')




