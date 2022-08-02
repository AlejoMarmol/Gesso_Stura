# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 10:03:22 2022

@author: clemo
"""
import pandas as pd

# cvs file
input_permeability = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/permeability/capacita_uso_suoli_con_drenaggio_con_consorzi.csv"
input_cadastre = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/cadastre/Intersection_uso_suolo_agri_consorzi_web.csv"

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
dict_change_crops = {
          'Altra Superficie': 'null',
          'Altra arboricoltura da legno': 'arbori',
          'Boschi': 'Prato',
          'Cereali': 'Mais',
          'Foraggere avvicendate': 'Prato',
          'Fruttiferi': 'Frutteto' ,
          'Ortive': 'Ortive in piena aria',
          'Patata': 'Patata',
          'Vivai': 'arbori',
          '_N.D.' : 'null',
          'Pioppeti':'arbori',
          'Prati permanenti e pascoli' : 'Prato',
          'Orti familiari': 'Ortive in piena aria',
          'Terreni a riposo' : 'null',
          'Legumi secchi' : 'Legumi secchi',
          'Piante industriali':'null',
          'Fiori e piante ornamentali':'arbori',
          }
# %% =========================================================================
# dataframe consortium intersect with comuni
# ============================================================================
def collect_all_information():
    """
    Collect all the information for the crops and for the permeability matrix for 
    all the consortium
    ----------------------
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
    consortia = []
    return(collect_information_consortium(consortia))

# %% =========================================================================
# collect info consorzi
# ============================================================================
def collect_information_consortium(consortia):
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
        
    ----------------------
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
    # test if it is list of consortium or not
    if type(consortia) is not list :
            consortia = [consortia]
            
    # test if the consortia list is empty
    if consortia == []:
        # if it is empty it mean we want to get the info for all the consortia
        all_info = True
    else :
        all_info = False
        
    # # -------------------- Collect the data for crops------------------------   
    # Collect the data related to the intersection consortium - comuni
    df_consor_n_cada = intersection_cadastre_consorzi(consortia, all_info)

    
    # # ---------------- Collect the data of permeability ---------------------
    df_permeability = collect_data_permeability(consortia, all_info)
       
    
    # # --------- Creation of the dict which contains the results -------------
    consortia  =  df_permeability.consor_nome.tolist()
        
    # ------------------------------
    """create the output for the crops based on a dict, 
    where key = consortium, sub_key =  type of crop"""
    dict_crops = dict.fromkeys(consortia, 0)
    # ------------------------------
    """create the output for the permeability matrix based on a dict, 
    where key = consortium, sub_key = place in the matric"""
    dict_matrix_consor = dict.fromkeys(consortia, 0)

    # ------------------------------
    
    for consortium in consortia :
        
        # ------------------------------
        # #for the crops and superficy
        df_consor_crop = df_consor_n_cada[(df_consor_n_cada.DENOMINAZI == consortium)]
        
        df_sum_crop = df_consor_crop.groupby(by = ['cens_liv3']).sum()
        dict_crops_consor = df_sum_crop['particella'].to_dict()
        
        # organize crops 
        dict_crops[consortium] = organize_crops(dict_crops_consor)
        
        # ------------------------------
        # for the permeability
        df_consor_perm = df_permeability[(df_permeability.consor_nome == consortium)]
        df_sum_perm = df_consor_perm.groupby(by=['dren','cuso']).sum()
        # round the value to 2 decimal 
        df_sum_perm['inter_perma_area_%'] = df_sum_perm['inter_perma_area_%'].round(decimals = 2)
        dict_perm_consor = df_sum_perm['inter_perma_area_%'].to_dict() 
        
        # obtain the matrix 
        dict_matrix_consor[consortium] = create_permeability_matrix(dict_perm_consor)
      
    
    
    return(dict_crops, dict_matrix_consor)
 
# %% =========================================================================
# collect info for the crops
# ============================================================================
    
def intersection_cadastre_consorzi(consortia, all_info=False):
    """
    get the consortia inside the the file input cadastre
        
    Parameters local : 
    ----------------------
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
    df_consor_n_cada = pd.read_csv(input_cadastre,
                                     encoding = 'utf-8', sep = ',')
          
    # do we want all the consortium ? 
    if all_info == False :
        df_consor_n_cada = df_consor_n_cada[df_consor_n_cada['DENOMINAZI'].isin(consortia)]

    return(df_consor_n_cada)


def organize_crops(dict_crops):
    """
    associate each type of crops coming from geoportal to a type of crops used
    in quant 4
    
    Parameters local : 
    ----------------------
    dict_crops : dictionnary 
        key : type of crops from geoportal
        value : area associated with each type of crops 
        
    Parameters global : 
    ---------------------- 
    dict_change_crops : dictionnary
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
    for key in dict_crops.keys():
        # get the crop of quant 4 associate with the crops of geoportal
        if key not in dict_change_crops.keys():
            print(key +' of dict_crops not a key of dict change crops')
        crops_quant4 =  dict_change_crops[key]
        
        # if the crop of quant 4 aleady in the output dict we had the area value 
        if crops_quant4 in dict_crops_quant4.keys():
            dict_crops_quant4[crops_quant4] += dict_crops[key]
            
        # else we create a new element in the dict
        else :
            dict_crops_quant4[crops_quant4] = dict_crops[key]
            
    return dict_crops_quant4
            

# %% =========================================================================
# collect info for the permeability
# ============================================================================
    
def collect_data_permeability(consortia, all_info=False):
    """
    collect the database containing the permeability and the type of soil for 
    each consortium
        
    Parameters local : 
    ----------------------
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
    df_permeability = pd.read_csv(input_permeability,
                                     encoding = 'utf-8', sep = ',')
    
    # control if the file has the right name for the column
    columns_name = ['consor_nome','AGGREGATO', 'consor_area','inter_perma_area',
                        'fk_cuso','fk_dren']
    
    for columns in columns_name :
        if columns not in df_permeability :
            print('''Error : the file doesn't have the right name for the columns,
                      the name should be :'consor_nome','AGGREGATO', 'consor_area',
                      'inter_perma_area','fk_cuso','fk_dren' ''')
            
    # Select the consortium we want 
    if all_info == False :
        df_permeability = df_permeability[df_permeability['consor_nome'].isin(consortia)]
    
    
    # # --------------------- organize for the matrice ------------------------
    
    # order the dataframe by the consortium and the permeability and the soil
    df_permeability = df_permeability.sort_values(by=['consor_nome', 
                                                      'fk_cuso','fk_dren'])
    # use the dict_perm to associate each value of dren and cuso with the one 
    # in the matrix of quant 4
    df_permeability['dren'] = df_permeability['fk_dren'].map(dict_perma_dataset['dren'])
    df_permeability['cuso'] = df_permeability['fk_dren'].map(dict_perma_dataset['cuso'])
                   
    # # --------------------- Calculate the percentage ------------------------
    # # --------- cover by each intersection dren_capcity_consortium ----------
    ratio  = df_permeability['inter_perma_area']/df_permeability['consor_area']
    df_permeability['inter_perma_area_%'] = round(ratio*100,3)
    
    
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


# %% =========================================================================
# Writting test
# ============================================================================
    
if __name__ == '__main__': 
    
    # --------------------------------------------
    # test for one consortia
    consortia = 'PARTECIPANZA BEALERA GROSSA DI CUNEO'
    dict_crops_1, dict_perma_1  = collect_information_consortium(consortia)
    
    # --------------------------------------------
    # test for all the consortia
    dict_crops_2, dict_perma_2  = collect_all_information()
