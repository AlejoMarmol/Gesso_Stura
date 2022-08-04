# import the shape file 
path = "D:/StudioPD/cherasco/Clement/INPUT/"
cadastre_name_file = "CADASTRIAL_UNITS_CHERASCO.shp"

# consortia layer and plot
cadastre_layer = QgsVectorLayer( path+ cadastre_name_file, "cadastrial_units_Cherasco", "ogr")
QgsProject.instance().addMapLayer(cadastre_layer)

idx = cadastre_layer.fields().indexOf('cens_liv4')
values = cadastre_layer.uniqueValues(idx)
                
print(values)