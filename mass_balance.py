# -*- coding: utf-8 -*-
"""
Created on Thu May 19 09:32:00 2022

@author: clemo
"""
# usual library 
import pandas as pd
import numpy as np

# import class function
import river_structure as rv 

from tkinter import *

# %%
# print the river 

class ZoneAffichage(Canvas):
    def __init__(self,parent,w,h):
        Canvas.__init__(self,master=parent,width=w, height=h, bg='black')
        self.__balles = []
        self.__job = None
        
        
# creation of the interaction frame  
class FenPrincipal(Tk):
    
    def __init__(self):
        Tk.__init__(self)
        self.title = "River mass balance"
        
        #         
        self.fenetre = Frame(self,bg='black')
        self.fenetre.pack()
        
        self.__zoneAffichage = ZoneAffichage(self,500,400)
        self.__zoneAffichage.pack(side=TOP, padx=5, pady=5)

        
# %% Test the classes
if __name__ == '__main__':
    