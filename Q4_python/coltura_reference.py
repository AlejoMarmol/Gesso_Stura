import pandas as pd
import xlrd
import xlwt


# %% ===========================================================================
#                         Dictionnary of coordinate for excel
# ==============================================================================
list_non_desired_crop = ['ORZO','_N.D.','NULL',
                         'FRUMENTO TENERO E SPELTA',
                         'ALTRA SUPERFICIE',
                         'FRUMENTO DURO',
                         'TERRENI A RIPOSO, SENZA AIUTO',
                         'NOCCIOLO']



dict_coordinate_crops = {
                        'Coltura': [0,1],     #B1
                        'kc' :{'apr': [2,4],  #E3
                               'mag': [2,5],  #F3
                               'giu': [2,6],  #G3
                               'lug': [2,7],  #H3
                               'ago': [2,8],  #I3
                               'set': [2,9],  #J3
                              } ,                    
                        'kr' :{'apr': [3,4], #E4
                               'mag': [3,5], #F4
                               'giu': [3,6], #G4
                               'lug': [3,7], #H4
                               'ago': [3,8], #I4
                               'set': [3,9], #J4
                              } ,     
                        'FN potenziali di valore medio' :{'apr': [4,4],  #E5
                                                          'mag': [4,5],  #F5
                                                          'giu': [4,6],  #G5
                                                          'lug': [4,7],  #H5
                                                          'ago': [4,8],  #I5
                                                          'set': [4,9],  #J5
                                                         }     ,                            
                        'FN potenziali con fred di superamento' :{'apr': [5,4],  #E6
                                                                  'mag': [5,5],  #F6
                                                                  'giu': [5,6],  #G6
                                                                  'lug': [5,7],  #H6
                                                                  'ago': [5,8],  #I6
                                                                  'set': [5,9],  #J6
                                                                 } 
                        }

# %% ===========================================================================
#                              Tool function
# ==============================================================================
class Excel_reference_coltura():
    
    def __init__(self, name) :
        # ----------------------
        # Create the excel file
        self.name = name
        
        #workbook and sheet
        self.workbook = xlrd.open_workbook(self.name)
        self.sheet = self.workbook.sheet_by_index(0)
        
        # -----------------------------------------
        #  Create the dict which has all the info 
        self.dict_coordinate = dict_coordinate_crops        
        
        
    # ==========================================================================
    def get_reference_coltura(self):
        """
        get the name of the coltura reference inside the excel file
        the aim is to go throughtout the excel file and finally retuns
        the name of each coltura with the row of their cell
        ------------
        Returns
        
        dict_coltura_reference : dictionnary
            key : referenced  coltura
            value : the ligne of the cell of the reference coltura
        """
        dict_coltura_reference = {}
        row_coordinate  = self.dict_coordinate['Coltura'][0]
        
        # get the first reference coltura 
        value = self.sheet.cell_value(row_coordinate, 
                                      self.dict_coordinate['Coltura'][1])
        
        # write the value inside the dictionnary 
        dict_coltura_reference[value] = row_coordinate
        
        # go to the next coltura 
        row_coordinate += 10
        
        while row_coordinate < self.sheet.nrows :
            
            # get the next reference coltura 
            value = self.sheet.cell_value(row_coordinate, 
                                          self.dict_coordinate['Coltura'][1])
                                      
            # write the value inside the dictionnary 
            dict_coltura_reference[value] = row_coordinate
            
            # go to the next coltura 
            row_coordinate += 10
            
            
        return dict_coltura_reference
    
    # ==========================================================================
    def get_info_coltura(self, coltura, row):
        """
        get all the information of a reference coltura by reading the excel
        ------------
        Parameters 
        
        coltura : string 
            name of the coltura
        
        row : value
            the row of where the name of the coltura is written
            
        Returns
        
        dict_info_coltura : dictionnayr
            store all the info concerning the crops 
            key : type of info 
        """   
        dict_info_coltura = {}
        
        for type in self.dict_coordinate.keys():

            dict_info_coltura[type] = {}
            
            if type != 'Coltura':
                for month in self.dict_coordinate[type].keys():
                    
                    # get the next reference coltura 
                    value = self.sheet.cell_value(row + self.dict_coordinate[type][month][0]  , 
                                                  self.dict_coordinate[type][month][1])   
                
                    dict_info_coltura[type][month] = value 
            

    
        return dict_info_coltura
    # ==========================================================================
    
    def collect_all_information(self, list_non_reference_crop):
        """
        collect the info of a reference crop
        If a crop is not written inside the database, raise an error
        ------------
        Parameters
        
        list_non_reference_crop : lits
            liste of the crop for which the users wants to collect the data
        
        -----------
        Returns
        
        dict_info_coltura : dict
            key : crop
            value : value of the crop 
        
        """
        dict_info_coltura = {}
        
        # collect the list of referenced crops 
        dict_coltura_reference = self.get_reference_coltura()
        
        for crop in list_non_reference_crop :
            
            # test if the dop is referencec
            if crop in dict_coltura_reference.keys() :
                dict_info_coltura[crop] = self.get_info_coltura(crop, dict_coltura_reference[crop])
                
            
            else :
                if crop not in  list_non_desired_crop : 
                    raise(ValueError('The crop : '+ crop + ' is not referenced in the file : ' + self.name + '.Please either add in the excel file.'))
         
        return dict_info_coltura 
        


# %% ===========================================================================
#                              Writting test
# ==============================================================================    
"""
    
name = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/Quant4/Coltura_reference.xlsx"

Excel_coltura = Excel_reference_coltura(name)

dict_coltura_reference = Excel_coltura.get_reference_coltura()

dict_info_coltura = Excel_coltura.get_info_coltura('Ortive in piena aria',
                                                    dict_coltura_reference['Ortive in piena aria'])

results = Excel_coltura.collect_all_information(['Ortive in piena aria'])
"""
    
    
    
    