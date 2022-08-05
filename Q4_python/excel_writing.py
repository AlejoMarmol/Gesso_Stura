# -*- coding: utf-8 -*-
"""
Created on Thu May 26 11:54:59 2022

@author: clemo
"""


import pandas as pd
import xlrd
import xlwt
import shutil  
import time
start_time = time.time()

# %% ==========================================================================
#                         Dictionnary of coordinate for excel
# =============================================================================

dict_coordinate = {
        'Denominaz.ne' : [12,2],  # C13
        'Numero Consorziati'  :[18,3],#D19
        'Superficie irrigata' :[18,7],# H19
        'Inizio'   : [20,7],# H21
        'Terminea' : [20,10],# K21
        'Composizione rete irrigua collettiva (in % della lunghezza totale)' :
            {'Canali in terra' : [23,3], #D24
             'Canali rivestiti e simili' : [23,7], # H24
             'Condotte' : [23,10]# K24
             }, 
        'Composizione rete irrigua aziendale (in % della lunghezza totale)' :
            {'Canali in terra' : [26,3],#D27
             'Canali rivestiti e simili' : [26,7] ,# H27
             'Condotte' : [26,10] # K27
            },
        'Permeabilità' : {
            ('Bassa','1-2' ): [32,2], #C33
            ('Bassa','3'   ): [33,2], #C34
            ('Bassa','4'   ): [34,2], #C35
            ('Media','1-2' ): [32,3], #D33
            ('Media','3'   ): [33,3], #D34
            ('Media','4'   ): [34,3], #D35
            ('Alta' ,'1-2' ): [32,4], #E33
            ('Alta' ,'3'   ): [33,4], #E34
            ('Alta' ,'4'   ): [34,4]  #E35
                },
        'Colture irrigate' : {
                'Coltura' : [45,1] , #B46
                'Metodo irriguo' : [45,2] , #C46
                'Superf. irrigata (ha)' : [45,3] , #D46
                'Stagione irrigua' : 
                    {'inizio': [45,4] , #E46
                     'fine'  : [45,5] }#F46
                }, #end line 54
        'Fabbisogni netti parcellari di valore medio':
           {'coltura': [63,1] ,#B64
            'apr' : [63,5] ,#F64
            'mag' : [63,6] ,#G64
            'giu' : [63,7] ,#H64
            'lug' : [63,8] ,#I64
            'ago' : [63,9] ,#J64
            'set' : [63,10] #K64
                }, # end line 72
        'Fabbisogni netti parcellari con frequenza di superamento 20% (altezze mensili)':
            {'coltura': [122,1] ,#B123
            'apr' : [122,5] ,#F123
            'mag' : [122,6] ,#G123
            'giu' : [122,7] ,#H123
            'lug' : [122,8] ,#I123
            'ago' : [122,9] ,#J123
            'set' : [122,10] #K123
            }, # end line 131
        'Durata mensile dei prelievi (giorni)':
            {'apr' : [193,5] ,#F194
             'mag' : [193,6] ,#G194
             'giu' : [193,7] ,#H194
             'lug' : [193,8] ,#I194
             'ago' : [193,9] ,#J194
             'set' : [193,10] #K194
             }, 
        'Coltura':
            {'Coltura 1' : [421,2] , #C422 # last coltura possible 5, gap de 10 line between two coltura
             'kc' : 
                 {'apr' : [423,5] ,#F424
                  'mag' : [423,6] ,#G424
                  'giu' : [423,7] ,#H424
                  'lug' : [423,8] ,#I424
                  'ago' : [423,9] ,#J424
                  'set' : [423,10] #K424
                  }, 
             'kr' : 
                 {'apr' : [424,5] ,#F425
                  'mag' : [424,6] ,#G425
                  'giu' : [424,7] ,#H425
                  'lug' : [424,8] ,#I425
                  'ago' : [424,9] ,#J425
                  'set' : [424,10] #K425
                  },   
             'FN potenziali di valore medio' : 
                 {'apr' : [425,5] ,#F426
                  'mag' : [425,6] ,#G426
                  'giu' : [425,7] ,#H426
                  'lug' : [425,8] ,#I426
                  'ago' : [425,9] ,#J426
                  'set' : [425,10] #K426
                  }, 
             'FN potenziali con fred di superamento' : 
                 {'apr' : [426,5] ,#F427
                  'mag' : [426,6] ,#G427
                  'giu' : [426,7] ,#H427
                  'lug' : [426,8] ,#I427
                  'ago' : [426,9] ,#J427
                  'set' : [426,10] #K427
                  },   
             'FN parcellari della coltura di valore medio' : 
                 {'apr' : [427,5] ,#F428
                  'mag' : [427,6] ,#G428
                  'giu' : [427,7] ,#H428
                  'lug' : [427,8] ,#I428
                  'ago' : [427,9] ,#J428
                  'set' : [427,10] #K428
                  }, 
             'FN parcellari della coltura con freq, sup 20' : 
                 {'apr' : [428,5] ,#F429
                  'mag' : [428,6] ,#G429
                  'giu' : [428,7] ,#H429
                  'lug' : [428,8] ,#I429
                  'ago' : [428,9] ,#J429
                  'set' : [428,10] #K429
                  }                 
              }
            } 
# %% =========================================================================
# dictionnary with irrigation date
# ============================================================================

dict_irrig_date = {
        'prato'                 : {'inizio': 'apr', 'fine' : 'set' },
        'mais'                  : {'inizio': 'mag', 'fine' : 'ago' },
        'frutteto'              : {'inizio': 'apr', 'fine' : 'set' },
        'null'                  : {'inizio': 'apr', 'fine' : 'ago' },
        'riso'                  : {'inizio': 'mag', 'fine' : 'ago' },
        }

dict_irrig_methodo = {
        'prato'                 : 'scorrimento',
        'mais'                  : 'scorrimento',
        'frutteto'              : 'scorrimento',
        'ortive in piena aria'  : 'scorrimento',
        'legumi Secchi'         : 'scorrimento',
        'null'                  : 'scorrimento',
        'riso'                  : 'somm. perm.'
        }

# %% =========================================================================
# Copy excel file 
# ============================================================================

def copy(workbook):

    sheet = workbook.sheet_by_index(0)
    
    workbook2 = xlwt.Workbook()
    sheet2 = workbook2.add_sheet('Quant4', cell_overwrite_ok=True)

    # calculate total number of rows and 
    # columns in source excel file
    mr = sheet.nrows
    mc = sheet.ncols
    
    # copying the cell values from source 
    # excel file to destination excel file
    for i in range (1, mr ):
        for j in range (1, mc ):
            # reading cell value from source excel file
            value = sheet.cell_value(i, j)
      
            # writing the read value to destination excel file
            sheet2.write(i, j, value)
      
    # saving the destination excel file
    return(workbook2, sheet2)
   
  
  
# %% =========================================================================
# Class EXCEL writting
# ============================================================================
            
class Excel_write():
    # ==========================================================================
    def __init__(self, name, name_output, Denominaz, numero_consorziati,Inizio,Terminea):
        # ----------------------
        # Create the excel file
        self.name = name
        
        # output file
        self.output_name = name_output
        
        #workbook and sheet
        wb = xlrd.open_workbook(self.name)
        self.workbook,self.sheet  = copy(wb)

#        self.sheet = self.workbook.get_sheet(0)
        
        
        # ----------------------------
        # Initialize the excel file
        " denominaz"
                
        self.sheet.write(dict_coordinate['Denominaz.ne'][0],
                         dict_coordinate['Denominaz.ne'][1],
                         Denominaz)
        " numero consortia"
        self.sheet.write(dict_coordinate['Numero Consorziati'][0],
                         dict_coordinate['Numero Consorziati'][1],
                         numero_consorziati)
        "Inizio"
        self.sheet.write(dict_coordinate['Inizio'][0],
                         dict_coordinate['Inizio'][1],
                         Inizio)       
        "Terminea"
        self.sheet.write(dict_coordinate['Terminea'][0],
                         dict_coordinate['Terminea'][1],
                         Terminea)
        

        # -----------------------------------------
        #  Create the dict which has all the info 
        self.dict_coordinate    = dict_coordinate
        self.dict_irrig_date    = dict_irrig_date
        self.dict_irrig_methodo = dict_irrig_methodo
        
        # -------------------------------------------------------
        # Create identification line for all the similiar input 
        self.coltura_irrigate_row = 45
        self.fabbisogni_netti_medio_row = 63
        self.fabbisogni_netti_20_row = 122
        self.new_coltura_row = 421
        
    # ==========================================================================        
    def add_composizione_irrigua_collectiva(self, terra, simili, condotte):
        """
        add the composizione of the irrigua collectiva
        
        ------------
        Parameters
        ------------       
        terra : number
            the percentage reprsenting the percentage of canali in terra 
            in the rete irrigua aziendale
            
        simili : number
            the percentage reprsenting the percentage of canali in rivestiti e simili
            in the ret irrigua aziendale    
            
         condotte : number
            the percentage reprsenting the percentage of  condotte 
            in the ret irrigua aziendale
            """
        "Terra"
        self.sheet.write(self.dict_coordinate['Composizione rete irrigua collettiva (in % della lunghezza totale)']['Canali in terra'][0],
                         self.dict_coordinate['Composizione rete irrigua collettiva (in % della lunghezza totale)']['Canali in terra'][1],
                         terra)
                         
        "rivestiti e simili"                 
        self.sheet.write(self.dict_coordinate['Composizione rete irrigua collettiva (in % della lunghezza totale)']['Canali rivestiti e simili'][0],
                         self.dict_coordinate['Composizione rete irrigua collettiva (in % della lunghezza totale)']['Canali rivestiti e simili'][1],
                         simili)       
                         
        "condotte "                 
        self.sheet.write(self.dict_coordinate['Composizione rete irrigua collettiva (in % della lunghezza totale)']['Condotte'][0],
                         self.dict_coordinate['Composizione rete irrigua collettiva (in % della lunghezza totale)']['Condotte'][1],
                         condotte)
                         
             
    # ==========================================================================             
    def add_composizione_irrigua_aziendale(self, terra, simili, condotte):
        """
        add the composizione of the irrigua aziedndale
        
        ------------
        Parameters
        ------------       
        terra : number
            the percentage reprsenting the percentage of canali in terra 
            in the rete irrigua aziendale
            
        simili : number
            the percentage reprsenting the percentage of canali in rivestiti e simili
            in the ret irrigua aziendale    
            
         condotte : number
            the percentage reprsenting the percentage of  condotte 
            in the ret irrigua aziendale
            """
        "Terra"
        self.sheet.write(self.dict_coordinate['Composizione rete irrigua aziendale (in % della lunghezza totale)']['Canali in terra'][0],
                         self.dict_coordinate['Composizione rete irrigua aziendale (in % della lunghezza totale)']['Canali in terra'][1],
                         terra)
                         
        "rivestiti e simili"                 
        self.sheet.write(self.dict_coordinate['Composizione rete irrigua aziendale (in % della lunghezza totale)']['Canali rivestiti e simili'][0],
                         self.dict_coordinate['Composizione rete irrigua aziendale (in % della lunghezza totale)']['Canali rivestiti e simili'][1],
                         simili)       
                         
        "condotte "                 
        self.sheet.write(self.dict_coordinate['Composizione rete irrigua aziendale (in % della lunghezza totale)']['Condotte'][0],
                         self.dict_coordinate['Composizione rete irrigua aziendale (in % della lunghezza totale)']['Condotte'][1],
                         condotte)
                         
    # ==========================================================================                         
    def add_permeability_matrix(self, dict_perma):
        """
        add the permeability coefficient inside the excel file 
        
        ------------
        Parameters
        ------------        
        dict_perma : dictionnary
            keys : ('Bassa','1-2'), the position inside the matrix of permeability
            value : teh ratio
        """
        for key in dict_perma.keys():
            self.sheet.write(self.dict_coordinate['Permeabilità'][key][0],
                             self.dict_coordinate['Permeabilità'][key][1],
                             dict_perma[key])
        return 
    
    # ==========================================================================    
    def add_coltura_irrigate_info(self, coltura):
        """
        add for one cultura its  stagione irrigua and methodo irriguo based on 
        two dictionnary : dict_irrig_date and dict_irrig_methodo
        
        ----------------      
        Parameters local
        ----------------
        coltura : string
            name of the coltura
            
        -----------------            
        Parmeters global 
        -----------------        
        dict_irrig_methodo : dictionary
            key : name of coltura
            value : methodo of irrigata
            
        dict_irrig_date : dictionnary
            key_1 : name of coltura
            key_2 : inizio or fine, for irrigation
            value : data of irrigation for inizio and fine 
            
        """
        # add the methodo irriguo
        self.sheet.write(self.coltura_irrigate_row,
                         self.dict_coordinate['Colture irrigate']['Metodo irriguo'][1],
                         dict_irrig_methodo['null'])
            
        # add the inizio stagione irrigua
        self.sheet.write(self.coltura_irrigate_row,
                         self.dict_coordinate['Colture irrigate']['Stagione irrigua']['inizio'][1],
                         self.dict_irrig_date[coltura]['inizio'])
                
        # add the inizio stagione irrigua
        self.sheet.write(self.coltura_irrigate_row,
                         self.dict_coordinate['Colture irrigate']['Stagione irrigua']['fine'][1],
                         self.dict_irrig_date[coltura]['fine'])
        
            
        
        return
    
    # ==========================================================================   
    def add_all_coltura_irrigate(self,dict_all_coltura, list_new_crops):
        """
        add all the information for all the coltura inside the dict_all_coltura
        
        ------------
        Parameters
        ------------        
        dict_all_coltura : dictionnary   
            key = name of the coltura
            value = superficie of irrigata
            
        """
        if self.coltura_irrigate_row > 55:
            raise(ValueError('Not enough place too add a coltura irrigate'))
            return 
        
        for coltura in dict_all_coltura :
            if coltura in self.dict_irrig_date.keys() : 
                 # add the name of the coltura
                 self.sheet.write(self.coltura_irrigate_row,
                                  self.dict_coordinate['Colture irrigate']['Coltura'][1],
                                  coltura)
                 
                 # add the surperficie 
                 self.sheet.write(self.coltura_irrigate_row,
                                  self.dict_coordinate['Colture irrigate']['Superf. irrigata (ha)'][1],
                                  dict_all_coltura[coltura])   
                 
                 # add the information of the coltura
                 self.add_coltura_irrigate_info(coltura)
                 
                 # increment the row to add the next coltura 
                 self.coltura_irrigate_row += 1
                 
            elif coltura in list_new_crops : 
                 # add the name of the coltura
                 self.sheet.write(self.coltura_irrigate_row,
                                  self.dict_coordinate['Colture irrigate']['Coltura'][1],
                                  coltura)
                 
                 # add the surperficie 
                 self.sheet.write(self.coltura_irrigate_row,
                                  self.dict_coordinate['Colture irrigate']['Superf. irrigata (ha)'][1],
                                  dict_all_coltura[coltura])   
                 
                 # add the information of the coltura
                 self.add_coltura_irrigate_info(coltura)
                 
                 # increment the row to add the next coltura 
                 self.coltura_irrigate_row += 1
    
    
    # ==========================================================================
    def add_fabbisogni_netti_20(self, coltura, dict_coltura_Fabbisogni_20):
        """
        add teh water need for the cultura, the one with 20% of rain
        
        ------------
        Parameters
        ------------        
        dict_Fabbisognia : dictionnary   
            key_1 = name of the coltura
            key_2 = month
            value = value of water need
            
        """
        if self.fabbisogni_netti_20_row > 132:
            raise(ValueError('Not enough place for coltura in Fabbisogni netti parcellari di netti 20%'))
            return 
        
        
        # add the coltura
        self.sheet.write(self.fabbisogni_netti_20_row,
                         self.dict_coordinate['Fabbisogni netti parcellari con frequenza di superamento 20% (altezze mensili)']['coltura'][1],
                         coltura)  
                         
        # add the methodo irriguo
        if coltura in self.dict_irrig_methodo : 
            self.sheet.write(self.fabbisogni_netti_20_row,
                             self.dict_coordinate['Colture irrigate']['Metodo irriguo'][1],
                             dict_irrig_methodo[coltura]) 
                             
        else :
            # the value by default of the irrigation method is scorrimento
            self.sheet.write(self.fabbisogni_netti_20_row,
                             self.dict_coordinate['Colture irrigate']['Metodo irriguo'][1],
                             'scorrimento') 
        
  
        # add the water need for each month
        for month in dict_coltura_Fabbisogni_20.keys():
            self.sheet.write(self.fabbisogni_netti_20_row,
                             self.dict_coordinate['Fabbisogni netti parcellari con frequenza di superamento 20% (altezze mensili)'][month][1],
                             dict_coltura_Fabbisogni_20[month])     
         
        # increment the row to add the next coltura 
        self.fabbisogni_netti_20_row += 1
        return

    # ==========================================================================
    def add_fabbisogni_netti_medi(self, coltura, dict_coltura_Fabbisogni_medi):
        """
        add teh water need for the cultura, the one with medi of rain
        
        ------------
        Parameters
        ------------        
        dict_Fabbisognia : dictionnary   
            key_1 = name of the coltura
            key_2 = month
            value = value of water need
            
        -----------------            
        Parmeters global 
        -----------------        
        dict_irrig_methodo : dictionary
            key : name of coltura
            value : methodo of irrigata
            
        """ 
        if self.fabbisogni_netti_medio_row > 73:
            raise(ValueError('Not enough place for coltura in Fabbisogni netti parcellari di valore medio'))
            return 
        
        # add the coltura
        self.sheet.write(self.fabbisogni_netti_medio_row,
                         self.dict_coordinate['Fabbisogni netti parcellari di valore medio']['coltura'][1],
                         coltura)
                         
        # add the methodo irriguo
        if coltura in self.dict_irrig_methodo : 
            self.sheet.write(self.fabbisogni_netti_medio_row,
                             self.dict_coordinate['Colture irrigate']['Metodo irriguo'][1],
                             dict_irrig_methodo[coltura]) 
                             
        else :
            print('************************')
            print( 'the coltura : '+ coltura +' does not have a method of')
            print('irriguo reference in dict_irrig_methodo,in the file')
            print(' : excel_writing.py the value by default will be :')
            print(' **scorrimento** ')
            print(' ')
            self.sheet.write(self.fabbisogni_netti_medio_row,
                            self.dict_coordinate['Colture irrigate']['Metodo irriguo'][1],
                            'scorrimento')
  
        # add the water need for each month
        for month in dict_coltura_Fabbisogni_medi.keys():
            self.sheet.write(self.fabbisogni_netti_medio_row,
                             self.dict_coordinate['Fabbisogni netti parcellari di valore medio'][month][1],
                             dict_coltura_Fabbisogni_medi[month])     
         
        # increment the row to add the next coltura 
        self.fabbisogni_netti_medio_row += 1
        return

    # ==========================================================================
    def add_new_coltura_fabisiogni(self, coltura_name, dict_new_coltura):
        """
        add fabisiogni neti medi and 20% of a non reference coltura
        non reference coltura means, it doesn't associated to prato, mais or 
        fruttteto
        ------------         
        Parameters
       
        coltura_name : string
            name of the new coltura we want
        
        dict_coltura_fabisiogni : dictionnary
            key_1 : fabisogni neti medi or fabisiogni neti 20%
            key_2 : month 
            value : value of the coefficient for the month 
        """
        self.add_fabbisogni_netti_medi(coltura_name, 
                                       dict_new_coltura['FN parcellari della coltura di valore medio'])
        self.add_fabbisogni_netti_20(coltura_name, 
                                       dict_new_coltura['FN parcellari della coltura con freq, sup 20'])
            
        
        
    # ==========================================================================
    def add_new_coltura(self, coltura_name, dict_new_coltura):
        """
        add a non reference coltura inside the excel file
        
        ------------
        Parameters
        coltura_name : string
            name of the new coltura we want
        
        dict_new_coltura : dictionnary
            key_1 : coefficent as k_c or FN potenziali con freq. di superamento 20% (mm)
            key_2 : month 
            value : value of the coefficient for the month 
        """
        
        if self.new_coltura_row > 461 :
            raise(ValueError('Not enough place to add a new type of coltura'))
            return
           
        else : 
            # write the new coltura 
            self.sheet.write(self.new_coltura_row,
                             self.dict_coordinate['Coltura']['Coltura 1'][1],
                             coltura_name) 
            
            self.new_coltura_row = 1 + self.new_coltura_row 
            
            # write the period of irrigation 
            self.add_irrigation_period_coltura(coltura_name, dict_new_coltura['kc'])
            
            # write the information of kc kr, etc
            for type in dict_new_coltura.keys(): 
                for month in dict_new_coltura[type].keys():
                    self.sheet.write(self.new_coltura_row,
                                     self.dict_coordinate['Coltura'][type][month][1],
                                     dict_new_coltura[type][month]) 
                
                # go to the next ligne of value
                self.new_coltura_row = 1 + self.new_coltura_row
            # go to the next coltura
            self.new_coltura_row = 2 + self.new_coltura_row 
            
            # add the value of fabisiogni netti medi and 20% with the similar 
            # of prato mais and frutteto
            self.add_new_coltura_fabisiogni(coltura_name, dict_new_coltura)
            
        return
        
        
    # ========================================================================== 
    def add_irrigation_period_coltura(self, coltura, dict_month):
        """
        add the irrigation periode for a new coltura 
        go throughout the dictionnary which contains the value of kc during the month, 
        and identify when the irrigation start and when it end 
        Then add the information directly in self.dict_irrig_date
        ------------
        Parameters
        
        dict_month  : dict 
            key : month 
            sub_key : month 
        ------------
        Returns
        
        """
        self.dict_irrig_date[coltura] = {}
        
        list_irrigate_month = []
        
        for month in dict_month.keys():
            if dict_month[month]!= 0:
                list_irrigate_month.append(month)
        
        # check if there is irrigation for this month 
        if list_irrigate_month == []: 
            # if there is no irrigated month, it meaning that the crop isn't useful for irrigation 
            raise(ValueError('The coltura : '  + coltura + ' has only null value for kc, Please add it in list_non_desired_crop inside coltura_reference.py'))
        else :
            # else add the name of irrigated month 
            self.dict_irrig_date[coltura]['inizio'] = list_irrigate_month[0]
            self.dict_irrig_date[coltura]['fine']   = list_irrigate_month[-1] 
            
            
        return 
    
    
    
""""
# %% ==========================================================================
#                                  Writting test
# =============================================================================
#__name__ = '__main__'
if __name__ == '__main__': 
    
    # python scrpits 

    import get_consortia_info_v2 as gci
    import get_water_need as gwn

    
    # -------------------------------------------------------------------------
    #                           Enter the name of the useful file
    # -------------------------------------------------------------------------
    #  path of  inputs  
    path = "C://Users/clemo/Documents/Italie/Studio PD/QGIS/info/"
    
    # ------------------------
    # consortia
    consortia_file = "consortia/CI_CORVA_SINISTRA.shp"
    
    # plot the consortia
    consortia_layer = QgsVectorLayer(path + consortia_file, "Consortia", "ogr")
    QgsProject.instance().addMapLayer(consortia_layer)
    
    # get the name of the consortia
    idx = consortia_layer.fields().indexOf('DENOMINAZI')
    list_consortia = list(consortia_layer.uniqueValues(idx))
    
    # ------------------------
    # file 
    permeability_file = path + "permeability/capacita_uso_suoli_con_drenaggio.shp"
    cadastre_file = path + "Cuneo_shapefile/all 2021.shp"
    polygone = path + consortia_file
    # -------------------------------------------------------------------------
    #                     Intersection between info file and the polygon
    # -------------------------------------------------------------------------
    # cadastre and polygon 

    poly_cadastre =  "poly_cadastre.shp"
    output_cadastre = intersection(polygone, cadastre_file, path + poly_cadastre)
    print('************************')
    print('Cadastre file created ')
    print(" %s seconds " % (time.time() - start_time))

    cadastre_layer = QgsVectorLayer(output_cadastre, "Cadastre", "ogr")
    QgsProject.instance().addMapLayer(cadastre_layer)
    
    # ------------------------
    # permeability and polygon 
    poly_permeability =  "poly_permability.shp"
    output_permeability = intersection(polygone, permeability_file, path + poly_permeability)
    
    permea_layer = QgsVectorLayer(output_permeability, "Permeability", "ogr")
    # calculate the ratio of type of soil on area of the consortia
    name_field = "Ratio_%"
    expression = '$area/"AREA_HA/10000"'
    add_field(permea_layer, name_field, expression)
    
    QgsProject.instance().addMapLayer(permea_layer)
    
    print('************************')
    print('Permeability file created ')
    print(" %s seconds " % (time.time() - start_time))
 
    # -------------------------------------------------------------------------
    #                              Initiate the clas
    # --------------------------------------------------------------------------
    name = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/Quant4/quant4_vers_4_2_xls_ORIGINALE.xls"
    Inizio = '01/04'
    Terminea = '30/09'
    Ex_write = Excel_write(name, 
                           dict_coordinate, 
                           list_consortia[0],
                           6.064,
                           Inizio,
                           Terminea)

    print('************************')
    print('Exceel file initialize ')
    print(" %s seconds " % (time.time() - start_time))
        # Save
    
    # --------------------------------------------------------------------------
    #                              get consortia info
    # -------------------------------------------------------------------------- 
  
    dict_crops, dict_perma  = collect_information_consortium(path,
                                                             cadastre_layer,
                                                             permea_layer,
                                                             list_consortia)
    print('************************')
    print('Info consortia')
    print(" %s seconds " % (time.time() - start_time))
    # ------------------------------------------------
    # Add permeability data
    consortia = list_consortia[0]
    dict_perma = dict_perma[consortia]
    Ex_write.add_permeability_matrix(dict_perma)
    
    # --------------------------------------------------------------------------
    #                           get monthly water need
    # -------------------------------------------------------------------------- 
    
    # get all the crops inside the polygons
    list_crop = get_list_crops(path, path + consortia_file, path + poly_cadastre)

    # ------------------------------------------------
    # centroids of polygon
    centroids_output = path + "centroids.shp"
    centroids_output = centroids( polygone, False, centroids_output)
    
    centroids_layer = QgsVectorLayer(centroids_output, "Centroids", "ogr")
    QgsProject.instance().addMapLayer(centroids_layer)
    # ------------------------------------------------
    # water need for each crop 
    dict_Fabbisogni_50, dict_Fabbisogni_20 = get_all_crops_needs(list_crop, 
                                                                  centroids_output,
                                                                  path+"Georeference/")
    
    print('************************')
    print('Water need')
    print(" %s seconds " % (time.time() - start_time))
    
    # Add the coltura data
    dict_coltura = {
        'prato'                 : 100,
        'mais'                  : 200,
        'frutteto'              : 300,
        'ortive in piena aria'  : 400,
        'legumi Secchi'         : 500,
        'riso'                  : 600
        }
    Ex_write.add_all_coltura_irrigate(dict_coltura)
    
    # Add water need for cotura 
    Ex_write.add_fabbisogni_netti_medi(dict_Fabbisogni_50)
    Ex_write.add_fabbisogni_netti_medi(dict_Fabbisogni_20)
    
    # Add a new coltura 
    dict_new_coltura = {
            'kc' : {'apr' : 1 , 'mag' : 1 , 'giu' : 1 ,'lug' : 1  ,'ago' : 1 ,'set' : 1 }, 
            'kr' : {'apr' : 1 , 'mag' : 1 , 'giu' : 1 ,'lug' : 1  ,'ago' : 1 ,'set' : 1 },  
            'FN potenziali di valore medio (mm)' :
                {'apr' : 1 , 'mag' : 1 , 'giu' : 1 ,'lug' : 1  ,'ago' : 1 ,'set' : 1 }, 
            'FN potenziali con freq. di superamento 20% (mm)' : 
                {'apr' : 1 , 'mag' : 1 , 'giu' : 1 ,'lug' : 1  ,'ago' : 1 ,'set' : 1 },                
                }
    coltura_name  = 'chien'
    Ex_write.add_new_coltura(coltura_name, dict_new_coltura)
    Ex_write.add_new_coltura(coltura_name, dict_new_coltura)

    print('************************')
    print('End programm')
    print(" %s seconds " % (time.time() - start_time))

"""