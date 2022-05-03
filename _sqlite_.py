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
dict_crops, dict_perma = rcs.collect_information_consortium(['PARTECIPANZA CANALE ROERO',
                                                          '1° DISTRETTO IRRIGUO ELETTRICO FERNANDO OLIVERO DI VIGNOLO E CREVASCA',
                                                          'PARTECIPANZA CANALE MORRA',
                                                          'PARTECIPANZA CANALI MIGLIA E VIGNOLO'],True)
#
# create a new dataframe
# 
df_crops = pd.DataFrame(dict_crops).T      
df_perma = pd.DataFrame(dict_perma).T
 
# merge in one
df_quant4_consor = pd.merge(df_crops, df_perma, 
                            left_index = True, right_index = True)
                                                   
#
# Open the connexion with the data base or create the data base 
#
conn = sqlite3.connect('merge_test.sqlite')

sql = '''INSERT INTO projects(name, mais, fruits) VALUES(?,?,?)'''
cur = conn.cursor()


df_quant4_consor.to_sql("surveys2002", conn, if_exists="replace")

conn.close() 