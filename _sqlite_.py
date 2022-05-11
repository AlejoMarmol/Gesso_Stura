# -*- coding: utf-8 -*-
"""
Created on Tue May  3 15:52:29 2022

@author: clemo
"""

#
# import the acces module related to the data base 
#
import sqlite3
import pandas as pd
import _read_consortia_splitting as rcs

#
# extract the value from _read_consortia_splitting 
#
dict_crops, dict_perma, dict_superficy = rcs.collect_all_information()

#
# create a new dataframe
# 
df_crops = pd.DataFrame(dict_crops).T  
df_crops = df_crops.fillna(0)    
df_perma = pd.DataFrame(dict_perma).T
df_perma = df_perma.fillna(0) 
df_superficy = pd.DataFrame(dict_superficy).T
df_superficy = df_superficy.fillna(0) 

# merge in one
df_merge_1 = pd.merge(df_crops, df_perma,
                      left_index = True, right_index = True)

df_quant4_consor = pd.merge(df_merge_1, df_superficy,
                            left_index = True, right_index = True)                                                
#
# Open the connexion with the data base or create the data base 
#
conn = sqlite3.connect('merge_test.sqlite')

df_quant4_consor.to_sql("surveys2002", conn, if_exists="replace")

conn.close() 