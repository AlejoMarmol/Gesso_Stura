# ------------------------------------------------------------------------------
#                              Useful parameters 
# ------------------------------------------------------------------------------

dict_type_crop  ={
    '_N_D': 'null',
    '_N.D.': 'null',
    'Altra arboricoltura da legno' : 'null',
    'Altra Superficie' : 'null',
    'Altre coltivazioni legnose agrarie' : 'null',
    'Boschi' : 'prato',
    'Cereali' : 'prato',
    'Fiori e piante ornamentali' : 'frutteto',
    'Foraggere avvicendate' : 'prato',
    'Fruttiferi' : 'frutteto',
    'Legumi secchi': 'prato',
    'Olivo': 'mais',
    'Orti familiari' : 'mais',
    'Ortive' : 'mais',
    'Patata' : 'mais',
    'Piante industriali' : 'mais',
    'Prati permanenti e pascoli' : 'prato',
    'Pioppeti': 'mais',
    'Sementi e Piantine': 'mais',
    'Terreni a riposo' : 'null',
    'Vite' : 'null',
    'Vivai' : 'null'
    }

dict_month_crop = {
    'mais' : ['mag', 'lug', 'giu', 'ago'],
    'frutteto' : ['apr', 'mag', 'lug', 'giu', 'ago', 'set'],    
    'prato' : ['apr', 'mag', 'lug', 'giu', 'ago', 'set']
    }

# ******************************************************************************
#                          Intersection cadastre unit polygone
# ******************************************************************************


# ------------------------------------------------------------------------------
#                              intersection function  
# ------------------------------------------------------------------------------
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


# ------------------------------------------------------------------------------
#                              centroids  function  
# ------------------------------------------------------------------------------
def centroids(input, all_part, output):
    """
    calculate the centroids
    """
    # parameters 
    params ={'INPUT':input ,
             'ALL_PARTS':all_part,
             'OUTPUT': output}
    
    # calculate the centroids 
    outputdict = processing.run("native:centroids",params )
    
    return(outputdict['OUTPUT'])


# ------------------------------------------------------------------------------
#                   get the list of crops inside the polygone shapefile
# ------------------------------------------------------------------------------

def get_list_crops(path, polygone, cadastre, output="cadastre_inter.shp"):
    """
    extract the list of crops inside a polygons resulting from the intersection 
    between a polygone and the cadastre_unit file 
    
    -----------
    Parameters
    
    path : string  
        name of the folder in which the cadaste file the polygone file are store 
        ATTENTION : for now polygon and cadastre are in the same folder
    
    polygone : string 
        name of the shapefile for which you want to copute the water need
        ex 'Test_polygones.shp'
    
    cadastre : string 
        name of the cadastre unit file in which there are the cadastre crops units
    
    ouput : string 
        name of the ouput file in which the intersection will be store
        ex : output = "cadastre_inter.shp"
    """
    cadastre_inter = intersection(polygone, cadastre, path + output)
    cadas_layer = QgsVectorLayer(cadastre_inter, "cadastre", "ogr")


    # get the list of crops inside the polygone after the intersection with the cadatres
    idx = cadas_layer.fields().indexOf('cens_liv3')
    list_crop = list(cadas_layer.uniqueValues(idx))

    return list_crop


# ******************************************************************************
#                              Evaluate water need
# ******************************************************************************

# ------------------------------------------------------------------------------
#                   extract raster values at centroids
# ------------------------------------------------------------------------------
def extract_month_needs(month, crop, centroids, medi, wn):
    """
    calculate for a file containing centroids the water need associated to centroid
    for a specific month and type of crops
    
    -----------
    Parameters 
    
    month : string
        month for which we wanted the water need
        
    crop : string
        the type of crop for which we want the water need
        
    centroids : shapefile
        shapefile containing the points from which water needs will be assessed
        
    medi : folder name
        all to indicate if we compute the water need for medi or sup20
        and also indicate where are the raster  from which the water requirements
        will be extracted
 
    wn : folder name
        fodler where all the monthly water need shapefile will be store
    """    
    # select if we work with the file medi or the file sup20
    if "medi" in medi :
        name = "medi"
    else :
        name = "sup20"
    
    # raster file 
    raster = "FN_" + crop + "_" + name +"_"+ month + "_wn.tif"
    
    # output file 
    water_need_output = wn + crop + "_" + name + "_"  + month + "_water_need.shp"

    # raster sampling 
    parameter_sampling = {
        'INPUT': centroids,
        'RASTERCOPY' :  medi + raster,
        'COLUMN_PREFIX':month ,
        'OUTPUT': water_need_output}
      
    outputdict = processing.run("native:rastersampling", 
                        parameter_sampling)
    
    return(outputdict['OUTPUT'])
    
    
    
# ------------------------------------------------------------------------------
#                 get water need for a single type of crop
# ------------------------------------------------------------------------------
def get_single_crop_needs(type_crop, centroids_output, medi, wn):
    """
    get the water need for a single type of crop for all the month, based on a 
    centroids file from which the calculation are made
    
    -----------
    Parameters 
    
    type_crop : string
        the type of crop for which the water need is going to be computed
    
    centroids_output : shapefile
        shapefile containing the points from which water needs will be assessed
    
    medi : folder name
        all to indicate if we compute the water need for medi or sup20
        and also indicate where are the raster  from which the water requirements
        will be extracted
 
    wn : folder name
        fodler where all the monthly water need shapefile will be store
    """
    dict_month_wn = {}
    
    # select if we work with the file medi or the file sup20
    if "medi" in medi :
        name = "medi"
    else :
        name = "sup20"
    
    # considers all the irrigation month which are possible 
    for month in ['apr', 'mag', 'lug', 'giu', 'ago', 'set']: 
        
        # if month is in dict_month_crop it means that the crops need to be 
        # irrigated this month 
        if month in dict_month_crop[type_crop] : 
            # calculated the value of the monthly water need
            wn_month = extract_month_needs(month, 
                                           type_crop, 
                                           centroids_output,
                                           medi, 
                                           wn)
            wn_layer = QgsVectorLayer(wn_month ,
                                      type_crop + '_'+ name + '_'+  month  + "_wn",
                                      "ogr")
            
            # collect the value of the monthly water need 
            value = wn_layer.getFeature(0)
            dict_month_wn[month] = value.attribute(5)
        
        # if the month isn't in dict_month crops it means that the crops doesn't 
        # need to be irrigated to the water need is null
        else :
            dict_month_wn[month] = 0
            
        
    return dict_month_wn 
    
    
# ------------------------------------------------------------------------------
#                               water need for all crop
# ------------------------------------------------------------------------------ 
    
def get_all_crops_needs( list_crop, centroids_output, path):
    """
    calculate the water need for all of the crops inside
   
    -----------
    Parameters 
    
    list_crop : list of string
        all the crops for which we need to calculate the water need
    
    centroids_output : shapefile
        shapefile containing the points from which water needs will be assessed 
    """
    # create the dict which will contains the monthly water need for each type of crop
    dict_crop_wn_medi = {}
    dict_crop_wn_sup = {}
    list_non_reference_crop = []

    # look at all the crop in the polygon
    for crop in list_crop :
        # get the type of crop related to the crop
        type_crop = dict_type_crop[crop]
        
        # check if the calcul add already made for the type of crop
        # if not make the compuatation
        if type_crop not in dict_crop_wn_medi.keys():
            
            # check if the type of crop is referenced are not 
            if type_crop == 'null':
                print('*******************')
                print('the crop : ' + crop + 'is not associated to prato - frutteto - mais')
                list_non_reference_crop.append(crop)
            # if is reference hget the water related to the centroids and the type of crop
            else :
                # folder where the shapefile corresponding to the water need of the centroids will be store
                wn   =  path + "Water_need/"
                
               # folder where the raster water need medi are stored 
                medi = path + "F_medi_originali/"
                dict_crop_wn_medi[type_crop]= get_single_crop_needs(type_crop, 
                                                                    centroids_output,
                                                                    medi, 
                                                                    wn)
                # folder where the raster water need sup20 are stored  
                sup = path + "FN_sup20_originali/"
                dict_crop_wn_sup[type_crop]= get_single_crop_needs(type_crop,
                                                                   centroids_output, 
                                                                   sup, 
                                                                   wn)
                                                            
    return (dict_crop_wn_medi, dict_crop_wn_sup, list_non_reference_crop)

