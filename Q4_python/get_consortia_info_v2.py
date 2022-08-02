"""
Created on Thu Jun  9 10:03:22 2022

@author: clemo
"""
import pandas as pd
import os # This is is needed in the pyqgis console also
from qgis.core import *


# cvs file
# input_permeability = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/permeability/capacita_uso_suoli_con_drenaggio_con_consorzi.csv"
# input_cadastre = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/cadastre/consortia_intersecte_cadastre.shp"

# ratio of urbanization and canali inside qgis
Perc_urbanizzazione = 2.0
Perc_stradi_canali_ecc = 3.0

# dict for calculating the matrix
dict_perma_dataset = {'dren' : {1 : 'Alta' , 2 : 'Alta',
                                3 : 'Media',
                                4 : 'Bassa', 5 : 'Bassa', 6 : 'Bassa', 7 : 'Bassa', 8 : 'Bassa'},
                      'cuso' : {1 : '1-2', 2 : '1-2',
                                3 : '3',
                                4 : '4', 5 : '4', 6 : '4', 7 : '4', 8 : '4'}
                      }
              
# create the matrix of permeability based on a dictionnary
dict_perma_matrix  = {('Bassa','1-2'): 0 , ('Media','1-2'): 0 , ('Alta','1-2'): 0,
                      ('Bassa','3')  : 0 , ('Media','3')  : 0 , ('Alta','3')  : 0,
                      ('Bassa','4')  : 0 , ('Media','4')  : 0 , ('Alta','4')  : 0
                      }

# associate each type of crops with the type of crops desired in quant 4 
dict_type_crops = {
 'ACTINIDIA': 'null', # marcella
 'ALBICOCCO': 'frutteto',
 'ALTRA ARBORICOLTURA DA LEGNO': 'ALTRE COLTIVAZIONI LEGNOSES AGRARIE', 
 'ALTRA FRUTTA TEMPERATA': 'frutteto',
 'ALTRA SUPERFICIE': 'null',
 'ALTRE COLTIVAZIONI LEGNOSE AGRARIE': 'null',# marcella
 'ALTRE ORTIVE DI PIENO CAMPO': 'ORTIVE IN PIENA ARIA',
 'ALTRE ORTIVE IN ORTI STAB. O IND.':'ORTIVE IN PIENA ARIA',
 'ALTRE PIANTE DA SEMI OLEOSI': 'null',
 'ALTRE PIANTE INDUSTRIALI': 'null', # marcella
 'ALTRI CEREALI' : 'null',
 'ALTRI ERBAI': 'prato',
 'ALTRI ERBAI MONOFITI DI CEREALI': 'prato',
 'ALTRI LEGUMI SECCHI' : 'null', 
 'ALTRI PRATI AVVICENDATI': 'prato',
 'AVENA': 'null', # marcella
 'CANAPA': 'null', # marcella
 'CASTAGNO': 'null', # marcella
 'CILIEGIO': 'frutteto',
 'COLZA E RAVIZZONE': 'prato',
 'ERBA MEDICA': 'prato', 
 'FAGIUOLI SECCHI' : 'null',
 'FAVA': 'null', # marcella
 'FIORI E PIANTE ORNAMENTALI IN PIENA ARIA': 'null',
 'FIORI PROTETTI IN SERRA': 'null',  # marcella
 'FRUMENTO DURO': 'null',
 'FRUMENTO TENERO E SPELTA': 'null',
 'FRUTTA A GUSCIO, ALTRA': 'null',
 'GIRASOLE': 'null',
 'GRANTURCO A MATURAZIONE CEROSA': 'mais',
 'GRANTURCO IN ERBA': 'mais' ,
 'GRANTURCO': 'mais',  
 'LUPPOLO': 'null', # marcella
 'MANDORLO': 'null', # marcella
 'MELO': 'frutteto',
 'NETTARINA': 'frutteto',
 'NOCE': 'null', # marcella
 'NOCCIOLO': 'ALTRE COLTIVAZIONI LEGNOSES AGRARIE', # marcella
  NULL: 'null',
 '_N.D.': 'null',
 'OLIVO DA TAVOLA': 'null',
 'OLIVO PER OLIO': 'null',
 'ORTI FAMILIARI': 'null', 
 'ORZO': 'null',
 'PASCOLI': 'prato',
 'PATATA': 'null',
 'PERO': 'frutteto', 
 'PIANTE AROMATICHE, MEDICINALI E COND.': 'null', # marcella
 'PIOPPETI': 'null', # marcella
 'PISELLO SECCO': 'null',
 'POMODORO DA INDUSTRIA': 'null',
 'POMODORO DA MENSA' : 'null' , 
 'PRATI PERMANENTI': 'prato',
 'RISO': 'riso',
 'SEMENTI': 'null', # marcella
 'SEMI DI LINO': 'null',# marcella
 'SORGO': 'null',
 'SUSINO': 'frutteto', # marcella
 'TERRENI A RIPOSO, SENZA AIUTO': 'null',
 'SOIA': 'null',
 'VITE': 'null', # marcella
 'VIVAI,ALTRI': 'null',  # marcella 
 'VIVAI,PIANTE ORNAMENTALI': 'null', # marcella 
 'VIVAI, FRUTTIFERI': 'null' # marcella
 }
# %% =========================================================================
#                       Transform shapefile in csv file
# ============================================================================
def transform_shp_to_csv(path, layer):
    """
    transform a shapefile into csv file 
    
    Parameters
    -------------
    path : string
        path of the file 
    
    input_file : string
        layer which you will modify
    """
    # create the ouput file name
    output_csv = path + layer.name() + ".csv"
    
    # transform the file 
    QgsVectorFileWriter.writeAsVectorFormat(layer, 
                                            output_csv ,
                                            "utf-8",
                                            QgsCoordinateTransform(),
                                            "CSV")
    
    return output_csv 

# %% =========================================================================
#                       dataframe consortium intersect with comuni
# ============================================================================
def collect_all_information(path, layer_cadastre, layer_permeability, id_field_consortia):
    """
    Collect all the information for the crops and for the permeability matrix for 
    all the consortium
    ----------------------
    
    Parameters 
    ----------------------
    input_cadastre : shapefile 
        Shapefile which contains the cadastran units inside a polygons for which
        we are going to collect the information 
        
    input_permeability : shapefile
        Contains the permeability information inside the same polygons as previous 
    
    Returns :
    ----------------------
    dict_S_tot_crops : dictionnay
        key_1 = consortitum name 
        key_2 = type of crop
        value  = superficie of the crop
        
    dict_matrix_value : dictonnary
        key_1 = consortitum name
        key_2 = (type of dren, type of capacity) 
        value  = ratio inside the consortium
        
    dict_superficy : dictonnary
        key_1 = consortitum name
        key_2 = municipalities related to the consortium 
        value =  superficie of the consortium inside the city 
    -------
    """
    
    return(collect_information_consortium(path,
                                          layer_cadastre, 
                                          layer_permeability, 
                                          []))

# %% =========================================================================
#                           collect info consorzi
# ============================================================================
def collect_information_consortium(path, layer_cadastre, layer_permeability, consortia, id_field_consortia):
    """
    Collect the information concerning all the municpalities related to 
    the consortium. The information are : the crops, the surface area covered
    by the crops, area of the city and the name of the city
     
     
    Parameters local: 
     ----------------------
    consortia : list
        liste with the name of the consortium
     
    Parameters global : 
    ----------------------
    dict_perma_matrix : dictionnary
        dict whcih represents the matrix of permeability where all the coef are 
        set to 0
        

    Returns :
    ----------------------
    dict_S_tot_crops : dictionnay
        key_1 = consortitum name 
        key_2 = type of crops of quant 4
        value  = superficie of the crop
        
    dict_matrix_value : dictonnary
        key_1 = consortitum name
        key_2 = (type of dren, type of capacity) 
        value  = ratio inside the consortium

    -------
    """    
    # -------------------------------------------------------------------------
    #             Transform the shapefile in usefull file  (csv)
    # -------------------------------------------------------------------------
    cadastre_info = transform_shp_to_csv(path, layer_cadastre)
    permeability_info = transform_shp_to_csv(path, layer_permeability)
    
    
    # -------------------------------------------------------------------------
    #                             Check the input
    # -------------------------------------------------------------------------   
    
    # test if it is list of consortium or not
    if type(consortia) is not list :
            consortia = [consortia]
            
    # test if the consortia list is empty
    if consortia == []:
        # if it is empty it mean we want to get the info for all the consortia
        all_info = True
    else :
        all_info = False
        

    # -------------------------------------------------------------------------
    #                         Collect the data for crops
    # -------------------------------------------------------------------------
    # Collect the data related to the intersection consortium - comuni
    df_consor_n_cada = intersection_cadastre_consorzi(cadastre_info, 
                                                      consortia,
                                                      id_field_consortia, 
                                                      all_info)

    
    # -------------------------------------------------------------------------
    #                     Collect the data of permeability
    # -------------------------------------------------------------------------
    df_permeability = collect_data_permeability(permeability_info,
                                                consortia,
                                                id_field_consortia, 
                                                all_info)
       
    
    # -------------------------------------------------------------------------
    #             Creation of the dict which will contain the results
    # -------------------------------------------------------------------------
    consortia  =  df_permeability.DENOMINAZI.tolist()
        
    # ------------------------------
    """create the output for the crops based on a dict, 
    where key = consortium, sub_key =  type of crop"""
    dict_crops = dict.fromkeys(consortia, 0)
    # ------------------------------
    """create the output for the permeability matrix based on a dict, 
    where key = consortium, sub_key = place in the matric"""
    dict_matrix_consor = dict.fromkeys(consortia, 0)

    # -------------------------------------------------------------------------
    #                             Fetch the results
    # -------------------------------------------------------------------------
    for consortium in consortia :
        
        # ------------------------------
        # #for the crops and superficy
        df_consor_crop = df_consor_n_cada[(df_consor_n_cada.DENOMINAZI == consortium)]
        
        df_sum_crop = df_consor_crop.groupby(by = ['cens_liv4']).sum()/10000 # 100000 conversion meters Ha
        dict_crops_consor = df_sum_crop['particella'].to_dict()
        
        # organize crops 
        dict_crops[consortium] = organize_crops(dict_crops_consor)
        
        # ------------------------------
        # for the permeability
        df_consor_perm = df_permeability[(df_permeability.DENOMINAZI == consortium)]
        df_sum_perm = df_consor_perm.groupby(by=['dren','cuso']).sum()
        # round the value to 2 decimal 
        df_sum_perm["Ratio_%"] = df_sum_perm["Ratio_%"].round(decimals = 2)
        dict_perm_consor = df_sum_perm["Ratio_%"].to_dict() 
        
        # obtain the matrix 
        dict_matrix_consor[consortium] = create_permeability_matrix(dict_perm_consor)
      
    
    
    return(dict_crops, dict_matrix_consor)
 
# %% ===========================================================================
#                               collect info for the crops
# ==============================================================================
    
def intersection_cadastre_consorzi(cadastre_info, consortia, id_field_consortia, all_info=False):
    """
    get the consortia inside the the file input cadastre
        
    Parameters local : 
    ----------------------
    cadastre_info: csv file
        contains all the info of the consortia 
        
    consortia : list
        liste with the name of the consortium
        
    all_info : booléen
        booléen which contains the information, do we want to extract the 
        information for all consortia
        
    Returns
    -------
    df_consor_n_cada : dataframe  
        contains all the data concerning the intersection between the consortium
        and the main crops per cadastrian unit
    """
    # # ------------------------- Collect the data ----------------------------    
    df_consor_n_cada = pd.read_csv(cadastre_info,
                                     encoding = 'utf-8', sep = ',')
    
    print(consortia)
    # do we want all the consortium ? 
    if all_info == False :
        df_consor_n_cada = df_consor_n_cada[df_consor_n_cada[id_field_consortia].isin(consortia)]

    return(df_consor_n_cada)


def organize_crops(dict_area_crops):
    """
    associate each type of crops coming from geoportal to a type of crops used
    in quant 4
    
    Parameters local : 
    ----------------------
    dict_area_crops : dictionnary 
        key : type of crops from geoportal
        value : area associated with each type of crops 
        
    Parameters global : 
    ---------------------- 
    dict_type_crops : dictionnary
        key : type of crops from geoportal 
        value : type of crops for quant 4
        
    Returns
    -------
    dict_crops_quant4 : dictonnary
        key : type of crops for quant 4
        value : area associated to the type of crops
    """
    # create the output dict
    dict_crops_quant4 ={}
    
    # look for the crops
    for key in dict_area_crops.keys():
        # get the crop of quant 4 associate with the crops of geoportal
        if key not in dict_type_crops.keys():
            print('*******************')
            raise(ValueError('the crop : ' + key +'is not reference in dict_type_crops in the program get_consortia_v2'))

        else : 
            if dict_type_crops[key] == 'null':
                crops_quant4 = key
            else : 
                crops_quant4 =  dict_type_crops[key]
        
        # if the crop of quant 4 aleady in the output dict we had the area value 
        if crops_quant4 in dict_crops_quant4.keys():
            dict_crops_quant4[crops_quant4] += dict_area_crops[key]
            
        # else we create a new element in the dict
        else :
            dict_crops_quant4[crops_quant4] = dict_area_crops[key]
            
    return dict_crops_quant4
            

# %% ===========================================================================
#                     collect info for the permeability
# ==============================================================================
    
def collect_data_permeability(permeability_info, consortia, id_field_consortia, all_info=False):
    """
    collect the database containing the permeability and the type of soil for 
    each consortium
        
    Parameters local : 
    ----------------------
    permeability_info: csv file
        Contains all the permeability information 
           
    consortia : list
        liste with the name of the consortium
        
    all_info : booléen
        booléen which contains the information, do we want to extract the 
        information for all consortia


    Parameters global : 
    ----------------------
    dict_perma_matrix : dict
        contains the link between the value of permeability and type of soil 
        with the value related to the matrix of permeability

    Returns
    -------
    df_permeability : dataframe  
        contains all the data concerning the intersection between the consortium
        the permeability and the quality of soil
    """
    
    # # ------------------------- Collect the data ----------------------------    
    df_permeability = pd.read_csv(permeability_info,
                                     encoding = 'utf-8', sep = ',')
    
    # control if the file has the right name for the column
    columns_name = [id_field_consortia,'Ratio_%',
                        'fk_cuso','fk_dren']
    
    for columns in columns_name :
        if columns not in df_permeability.columns :
            print('''Error : the file doesn't have the right name for the columns,
                      the name should be :'DENOMINAZI','AGGREGATO', 'AREA_HA','Ratio_%',
                        'fk_cuso','fk_dren' ''')
            
    # Select the consortium we want 
    if all_info == False :
        df_permeability = df_permeability[df_permeability[id_field_consortia].isin(consortia)]
    
    
    # # --------------------- organize for the matrice ------------------------
    
    # order the dataframe by the consortium and the permeability and the soil
    df_permeability = df_permeability.sort_values(by=[id_field_consortia, 
                                                      'fk_cuso','fk_dren'])
    # use the dict_perm to associate each value of dren and cuso with the one 
    # in the matrix of quant 4
    df_permeability['dren'] = df_permeability['fk_dren'].map(dict_perma_dataset['dren'])
    df_permeability['cuso'] = df_permeability['fk_dren'].map(dict_perma_dataset['cuso'])
                   
    # # --------------------- Calculate the percentage ------------------------
    # # --------- cover by each intersection dren_capcity_consortium ----------
#    ratio  = df_permeability['inter_perma_area']/df_permeability['consor_area']
    df_permeability["Ratio_%"] = round(df_permeability["Ratio_%"]*100,3)
    
    
    return(df_permeability)
    
    
def create_permeability_matrix(dict_consor_perm):
    """
    create the matrxi permeability of a consortium 
    
    Parameters local : 
    ----------------------
    dict_consor_perm : dictionnary 
        key : type of soil in the consortium as (Alta ; 1-2) or (Bassa ; 4)
        value : % of the type of soil in the consortium 
        
    Parameters global : 
    ---------------------- 
    dict_perma_matrix  : dictionnary
        key : matrix permeability position as  (Alta ; 1-2) or (Bassa ; 4)
        value : 0 for the initialization
        
    Returns
    -------
    dict_matrix_consor : dictonnary
        key : all type of soil comin from the matrix permeability  
        value : % of the type of soil in the consortium 
    """
    dict_matrix = dict_perma_matrix
    # full the dictionnary perma which correspond to the matrix of permeability
    for key in dict_perma_matrix.keys():
        if key in dict_consor_perm.keys():
            dict_matrix[key] = dict_consor_perm[key]

    return dict_matrix


# %% ===========================================================================
#                                Writting test
# ==============================================================================
    """
if __name__ == '__main__': 
    
    # --------------------------------------------
    #  path of  inputs  
    path = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/"
    
    # ------------------------
    
    # ------------------------
    # file 
    permeability_file = path + "permeability/capacita_uso_suoli_con_drenaggio.shp"
    cadastre_file = path + "Cuneo_shapefile/all 2021.shp"
    
    
    
    dict_crops_1, dict_perma_1  = collect_information_consortium(path, 
                                                                input_cadastre, 
                                                                input_permeability, 
                                                                [])
    
    # --------------------------------------------
    # test for all the consortia
    dict_crops_2, dict_perma_2  = collect_all_information()
"""