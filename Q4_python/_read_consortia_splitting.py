# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 10:34:31 2022

@author: clemo
"""

import pandas as pd

# cvs file
input_consortium = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/consortia/consorzi/consorzi_split_by_comuni.csv"
input_municipality = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/Agriculture-info/sasExportX14X.csv"
input_permeability = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/permeability/capacita_uso_suoli_con_drenaggio_con_consorzi.csv"
input_cadastre = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/cadastre/Intersection_uso_suolo_agri_consorzi_web.csv"

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
    return(collect_information_consortium(consortia, True))
    
# %% =========================================================================
# collect info consorzi
# ============================================================================   
def collect_information_consortium(consortia, all_info=False):
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
    #test if it is list of consortium or not
    if not all_info  : 
        if type(consortia) is not list :
            consortia = [consortia]
    
        
    # # -------------------- Collect the data for crops------------------------   
    # Collect the data related to the intersection consortium - comuni
    df_consor_n_comuni = intersection_consortium_comuni(consortia, all_info)
    
    list_comuni = df_consor_n_comuni.comune_nome.tolist()
       
    # extract the information concerning municipalities related to the consortium
    df_comuni = collect_data_crops_comuni(list_comuni)

    # Merge 
    df_merge = pd.merge(df_consor_n_comuni, df_comuni, on = 'comune_nome')

    # Calculate the surface covered by each crops inside the consortium 
    df_merge['Airr,cons'] = df_merge['Ratio_Superficie_crops']*df_merge['Area da usare']
    
    # # ---------------- Collect the data of permeability ---------------------
    df_permeability = collect_data_permeability(consortia, all_info)
       
    
    # # --------- Creation of the dict which contains the results -------------
    if all_info : 
        consortia  =  df_permeability.consor_nome.tolist()
        
    # ------------------------------
    """create the output for the crops based on a dict, 
    where key = consortium, sub_key =  type of crop"""
    dict_crops = dict.fromkeys(consortia, 0)
    # ------------------------------
    """create the output for the permeability matrix based on a dict, 
    where key = consortium, sub_key = place in the matric"""
    dict_consor_matrix = dict.fromkeys(consortia, 0)
    # ------------------------------
    """create the output for the superficy based on a dict,
    key = consortium, sub_key = municipaliti"""
    dict_superficy = dict.fromkeys(consortia, 0)
    # ------------------------------
    
    for consortium in consortia :
        # initalize the matrix of permeability to 0 value only "
        dict_matrix  = dict(dict_perma_matrix)
        
        # ------------------------------
        # #for the crops and superficy
        df_consor_crop = df_merge[(df_merge.consor_nome == consortium)]
        
        # for the superficy
        df_comune = df_consor_crop.groupby(by = ['comune_nome']).mean()
        dict_superficy[consortium] = df_comune['Area da usare'].to_dict()
        # add indication 
        name = 'Superficie_irrigabile_netta'
        dict_superficy[consortium] =  dict(("{}_{}".format(name,k),v) for k,v in dict_superficy[consortium].items())
        
        # for the crops
        df_sum_crop = df_consor_crop.groupby(by = ['crops']).sum()
        dict_crops[consortium] = df_sum_crop['Airr,cons'].to_dict()
        
        # ------------------------------
        # for the permeability
        df_consor_perm = df_permeability[(df_permeability.consor_nome == consortium)]
        df_sum_perm = df_consor_perm.groupby(by=['dren','cuso']).sum()
        # round the value to 2 decimal 
        df_sum_perm['inter_perma_area_%'] = df_sum_perm['inter_perma_area_%'].round(decimals = 2)
        dict_consor_perm = df_sum_perm['inter_perma_area_%'].to_dict() 
  
        # full the dictionnary perma which correspond to the matrix of permeability
        for key in dict_matrix.keys():
            if key in df_sum_perm['inter_perma_area_%'].index:
                dict_matrix[key] = dict_consor_perm[key]
        
        # add the dict perma inside the dict contains all the matrix of each consortium
        dict_consor_matrix[consortium] = dict_matrix
        
    
    
    return(dict_crops, dict_consor_matrix, dict_superficy)
    
 
# %% =========================================================================
# Collect all the data
# ============================================================================
    
         
def intersection_consortium_comuni(consortia, all_info=False):
    """
    find  all the municipalities related to the consortium and check if the 
    columns from the intersection between comuni and consortium have the right 
    name
        
    Parameters local : 
    ----------------------
    consortia : list
        liste with the name of the consortium
        
    all_info : booléen
        booléen which contains the information, do we want to extract the 
        information for all consortia
        
    Parameters global : 
    ----------------------
    Perc_urbanizzazione : float
        percentage of urbanization didn't take into account in the .shp file of
        the consortium
        
    Perc_stradi_canali_ecc : float
        percentage of stradi canali and other didn't take into account in the 
        .shp file of the consortium

    Returns
    -------
    df_consor_n_comuni : dataframe  
        contains the aggregato, the consortium are, the name of 
        comuni where the consortium, the area of the comune and the area of the 
        consortium inside each comune
    """
    # # ------------------------- Collect the data ----------------------------    
    df_consor_n_comuni = pd.read_csv(input_consortium,
                                     encoding = 'utf-8', sep = ',')
    
    # control if the file has the right name for the column
    columns_name = ['consor_nome','AGGREGATO', 'consor_area','comune_nome',
                        'comune_area','intersect_area']
    
    for columns in columns_name :
        if columns not in df_consor_n_comuni.columns :
            print('''Error : the file doesn't have the right name for the columns,
                      the name should be :'AGGREGATO', 'consor_area','consor_nome',
                      'comune_nome','comune_area','intersect_area' ''')
            
    # Select the consortium we want 
    if all_info == False : 
        df_consor_n_comuni = df_consor_n_comuni[df_consor_n_comuni['consor_nome'].isin(consortia)]
    
    
    # # ------------------------- arrange the data ----------------------------            
    # transform the name of the comuni to match with the other file
    list_comuni = df_consor_n_comuni.comune_nome.tolist()
    # Convert each string to uppercase because in df_comuni is in uppercase
    list_comuni = [comuni.upper() for comuni in list_comuni]
    
    df_consor_n_comuni['comune_nome'] = list_comuni
    
    # change the organisation of the columns
    df_consor_n_comuni = df_consor_n_comuni[columns_name]
    
    
    # # ------------------------- Calculation ---------------------------------    
    
    # Calculate the use area of the consortium inside the comune
    # due to urbanization road, etc which aren't take into account into QGIS
    
    df_consor_n_comuni['Superficie aree urbanizzate -comune'] = df_consor_n_comuni['intersect_area']*Perc_urbanizzazione/100
    df_consor_n_comuni['Superficie irrigabile lorda - comune [ha]'] = df_consor_n_comuni['intersect_area'] - df_consor_n_comuni['Superficie aree urbanizzate -comune']
    df_consor_n_comuni['Area da usare'] = (1-Perc_stradi_canali_ecc/100)* df_consor_n_comuni['Superficie irrigabile lorda - comune [ha]']


    return(df_consor_n_comuni)
    


    
    
def collect_data_crops_comuni(list_comuni, all_info=False):
    """
    read the database which contains all the information concerning the 
    crops inside each comuni related to a list of comuni
    
    Parameters: 
    ----------------------
    list_comuni : list of string
        contains all the comuni for which we want the information
        
    all_info : booléen
        booléen which contains the information, do we want to extract the 
        information for all consortia

    Returns
    -------
    df_comuni : dataframe 
        columns : municpalities - livello - Aziende con terreni - 
                  superficie total covered by each livello - anno - 
                  ratio surface : Surface_one_livello/Surace_municipality
                  percentage
    """
     
    df_all_comuni  = pd.read_csv(input_municipality,encoding = 'utf-16', sep = ',')

    # # ------------------------- Clear the datafrale-------------------------
    new_columns = ['comune_nome', 'crops', 'Aziende con terreni (n.)',
           'Superficie_crops_(ha)']

    # select your data
    df_comuni = df_all_comuni.iloc[2:, :4]

    # change the name of the columns
    df_comuni.columns = new_columns
    
    # reset the index to start a 0
    df_comuni.reset_index()
    
    # select only the municipalities we want
    if all_info == False :
        df_comuni = df_comuni[df_comuni['comune_nome'].isin(list_comuni)]
        

    # # ------------------------- Correct the data ----------------------------
    # transform str into float for the aziende and the superficie
    df_comuni['Aziende con terreni (n.)'] = df_comuni['Aziende con terreni (n.)'].astype(float)
    
    # *** reflace the point and the comma in the df in order to transforme the data in float ***
    df_comuni['Superficie_crops_(ha)'] = df_comuni['Superficie_crops_(ha)'].str.replace('.','')
    df_comuni['Superficie_crops_(ha)'] = df_comuni['Superficie_crops_(ha)'].str.replace(',','.')
    
    df_comuni['Superficie_crops_(ha)'] = df_comuni['Superficie_crops_(ha)'].astype(float)
    
 
    # # ------------------------- Calcultaion -------------------------------------
    # Calculate the surperficie total of all the crops for each municipality
    df_sum = df_comuni.groupby(['comune_nome']).sum()
    dict_superficie_tot = df_sum['Superficie_crops_(ha)'].to_dict()
    
    # create a new columns with the total superficie cover by crops in each municipality
    df_comuni['Superficie topografica consortile - comune [ha]'] = df_comuni['comune_nome'].map(dict_superficie_tot)

    # calculate the ratio that each crop cover in each municipality        
    df_comuni['Ratio_Superficie_crops'] = df_comuni['Superficie_crops_(ha)']/df_comuni['Superficie topografica consortile - comune [ha]']
    df_comuni['Percentage']    = round(df_comuni['Ratio_Superficie_crops']*100,2)
    
    # order the dataframe by the comune and the percentage
    df_comuni = df_comuni.sort_values(by=['comune_nome', 'Percentage'],
                                      ascending=False)
    
    # Report the anno 
    Anno = int(df_all_comuni.columns[2])
    df_comuni['Anno'] = Anno
    
    return(df_comuni)



def intersection_cadastre_consorzi(consortia, all_info=False):
    """
    find  all the municipalities related to the consortium and check if the 
    columns from the intersection between comuni and consortium have the right 
    name
        
    Parameters local : 
    ----------------------
    consortia : list
        liste with the name of the consortium
        
    all_info : booléen
        booléen which contains the information, do we want to extract the 
        information for all consortia
        

    """
    # # ------------------------- Collect the data ----------------------------    
    df_consor_n_cada = pd.read_csv(input_cadastre,
                                     encoding = 'utf-8', sep = ',')
          
    # Select the consortium we want 
    if all_info == False : 
        df_consor_n_cada  = df_consor_n_cada [df_consor_n_cada ['DENOMINAZI'].isin(consortia)]


    return(df_consor_n_cada)


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
    
    # arrange the columns
    df_permeability = df_permeability[columns_name]
    
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
            




    







