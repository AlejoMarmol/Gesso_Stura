# -*- coding: utf-8 -*-
"""
Created on Thu May 26 11:54:59 2022

@author: clemo
"""

# %% ==========================================================================
# Dictionnary of coordinate for excel
# =============================================================================

dict_coordinate = {
        'Denominaz.ne' : [13,1],  # B14
        'Numero Consorziati:'  :[18,3],#D19
        'Superficie irrigata:' :[18,7],# H19
        'Inizio'  : [20,7],# H21
        'Termino' : [20,10],# K21
        'Composizione rete irrigua collettiva (in % della lunghezza totale)' :
            {'Canali in terra' : [23,3], #D24
             'Canali rivestiti e simili' : [23,7], # H24
             'Condotte' : [23,10]# K24
             }, 
        'Composizione rete irrigua aziendale (in % della lunghezza totale):' :
            {'Canali in terra' : [26,3],#D27
             'Canali rivestiti e simili' : [26,7] ,# H27
             'Condotte' : [26,10] # K27
            },
        'Permeabilità' : {
            ('Bassa ','1-2' ): [32,2], #C33
            ('Bassa ','3'   ): [33,2], #C34
            ('Bassa ','4'   ): [34,2], #C35
            ('Media ','1-2' ): [32,3], #D33
            ('Media ','3'   ): [33,3], #D34
            ('Media ','4'   ): [34,3], #D35
            ('Alta  ','1-2' ): [32,4], #E33
            ('Alta  ','3'   ): [33,4], #E34
            ('Alta  ','4'   ): [34,4]  #E35
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
            {'apr' : [63,5] ,#F64
             'mag' : [63,6] ,#G64
             'giu' : [63,7] ,#H64
             'lug' : [63,8] ,#I64
             'ago' : [63,9] ,#J64
             'set' : [63,10] #K64
             }, # end line 72
        'Fabbisogni netti parcellari con frequenza di superamento 20% (altezze mensili)':
            {'apr' : [122,5] ,#F123
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
        'Coltura"':
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
             'FN potenziali di valore medio (mm)' : 
                 {'apr' : [425,5] ,#F426
                  'mag' : [425,6] ,#G426
                  'giu' : [425,7] ,#H426
                  'lug' : [425,8] ,#I426
                  'ago' : [425,9] ,#J426
                  'set' : [425,10] #K426
                  }, 
             'FN potenziali con freq. di superamento 20% (mm)' : 
                 {'apr' : [426,5] ,#F427
                  'mag' : [426,6] ,#G427
                  'giu' : [426,7] ,#H427
                  'lug' : [426,8] ,#I427
                  'ago' : [426,9] ,#J427
                  'set' : [426,10] #K427
                  },                  
              }
            } 
                 
# %% =========================================================================
# Class EXCEL writting
# ============================================================================
                 
class Excel_write():
    def __init__(self, name):
        self.name = name
        
        # Create identification line for all the similiar input 
        self.coltura_irrigate_number = 45
        self.fabbisogni_netti_medio_number = 63
        self.fabbisogni_netti_20_number = 122
        self.new_coltura_number = 421
        
    
    def add_coltura_irrigate(self, dict_coltura):
        
        self.coltura_irrigate_number += 1
        return


    def add_fabbisogni_netti_medio(self, dict_coltura):
        
        self.fabbisogni_netti_medio_number += 1
        return


    def add_fabbisogni_netti_20(self, dict_coltura):
        
        self.fabbisogni_netti_20_number += 1
        return


    def add_new_coltura(self, dict_coltura):
        
        self.new_colturae_number += 10
        return
                
                 