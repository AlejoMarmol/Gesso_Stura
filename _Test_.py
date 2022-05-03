from qgis.core import *
import qgis.utils 
import processing

"""
- comuni = the shp file which contains all the muncipalities
- consortium = the shp file  which contains the shape of the consortium we 
are working with
- output = the output file after the intersection

- 'qgis:intersection' : name of the algorithm 
"""
comuni  = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/municipalities/Comuni_cuneo_tutti_pol.shp"
consortium = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/consortia/Roero/Roreo.shp"
output = "merge.shp"


processing.runalg('qgis:intersection', consortium, comuni , "merge.shp")