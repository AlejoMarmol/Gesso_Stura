# -*- coding: utf-8 -*-
"""
Created on Mon May  9 14:07:58 2022

@author: clemo
"""

import pandas as pd
import copy
import collections

# # ------------------------- Name of the file --------------------------------  
input_node = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/QGIS_python/Nodi_BI_p.csv"
input_gesso = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/QGIS_python/gesso_BI_python_I.csv"
input_vermenagna = "C:/Users/clemo/Documents/Italie/Studio PD/QGIS/QGIS_python/Vermenagna_BI_python_I.csv"

# # ------------------------- Collect the data --------------------------------    
df_node = pd.read_csv(input_node, encoding = 'utf-8', sep = ',')
df_node = df_node.sort_values(by=['Nodo_num'])
df_node = df_node.fillna(0)   

river_gesso = 'gesso'
df_gesso = pd.read_csv(input_gesso, encoding = 'utf-8', sep = ',')
df_gesso['River'] = river_gesso

river_verme = 'vermenagna'
df_verme = pd.read_csv(input_vermenagna, encoding = 'utf-8', sep = ',')
df_verme['River'] = river_verme

df_section_rivers = pd.concat([df_gesso, df_verme])

# %%

# # -------------------------- class river ----------------------------------  
class River():
    def __init__(self,river, df_river):
        """
        init : 
            name of the river
            sections related to the river
            number of the node related to the river
        """
        self.name = river
        self.list_section = []
        self.list_node_number = []
        
        # create the section of the river
        for section_name in df_river['Tratto'].unique():
            section = Section(section_name,
                              df_river[df_river.Tratto == section_name])
                
            self.list_section.append(section)
            # add the starting node of the section inside the list of node owned by the river
            self.list_node_number.append(section.starting_number)
        
        self.list_node_number.append(section.ending_number)
        
    def set_river_name(self, new_name):
        self.name = new_name
        
    def set_section_list(self, list_section):
        self.list_section = list_section
    
    def set_node_number_list(self, list_node_number):
        self.list_node_number = list_node_number
        
    def create_copy(self):
        return copy.copy(self)

    def split_river(self,node_number):
        """
        split a river into based on a node, meaning there is a confluence
        
        Parameter 
        ----------------
        node_number : float
            node_number of the confluence which has to be in self.list_node
            
        Return
        ----------------
        list_river: list
            list which contains the rivers issued from the spliting of the main river
        
        """
        if node_number not in self.list_node_number :
            return('Error, the confluence node_number is not in the river')
        else : 
            index_split = self.list_node_number.index(node_number)
            
            # create the downstream river
            River_av = self.create_copy()
            River_av.set_river_name(self.name + '_av')
            River_av.set_section_list(self.list_section[index_split:])
            River_av.set_node_number_list(self.list_node_number[index_split:])
            
            # create the upstream river
            self.set_river_name(self.name + '_am')
            self.set_section_list(self.list_section[:index_split])
            list_node_number = self.list_node_number[:index_split]+ [self.list_node_number[index_split]]
            self.set_node_number_list(list_node_number)
            
            return [self, River_av]
    
    def create_Node(self, df_node):
        """
        Create the Node class associated to the river
        
        Parameters
        -------------
        df_node : dataframe
            
        """
        self.list_Node = []
    
        for node_name in df_node['Nodo_num'].unique():
            node = Node(node_name,
                        df_node[df_node['Nodo_num'].astype(int) == node_name])
            self.list_Node.append(node)  
                

# # -------------------------- class section ----------------------------------       
class Section():
    def __init__(self, river,  df_river, flow=None):
        self.river = river
        self.tratto = df_river['Tratto'].values[0]
        
        if flow == None:
            self.flow = df_river['Q'].values[0]
        else : 
            self.flow = flow
        
        " nodes related to the section, the information is contained in the "
        "tratto : 0-1 means starting node = 0 , and ending node = 1"
        list_node = self.tratto.split('-')
        self.starting_number = int(list_node[0])
        self.ending_number = int(list_node[1])
                
    def create_starting_node(self, df_node):
        """
        Create the Node class associated to the starting node of the section
        
        Parameters
        -------------
        df_node : dataframe
            
        """
        self.starting_Node = Node(self.starting_number,
                                df_node[df_node['Nodo_num'].astype(int) == self.starting_number])

                    
    def create_ending_node(self, df_node):
        """
        Create the Node class associated to the ending node of the section
        
        Parameters
        -------------
        df_node : dataframe
            
        """
        self.ending_Node = Node(self.ending_number,
                                df_node[df_node['Nodo_num'].astype(int) == self.ending_number])

                    
    def calculate_section_flow(self):
        """
        calculate the section flow based on the flow leaving of the starting node
        In the mean time set the flow coming at the ending_node
        """
        if self.starting_Node.subNode  :
            self.flow_section = self.starting_Node.subNode[-1].calculate_flow_out()
        else:
            self.flow_section = self.starting_Node.calculate_flow_out()
        
        if self.ending_Node.subNode  :
            self.ending_Node.subNode[0].set_flow_in(self.flow_section)
        else :
            self.ending_Node.set_flow_in(self.flow_section)
        
        return self.flow_section
            
# # --------------------------- class Node ------------------------------------
class Node():
    def __init__(self, number,df_node, confluence=False):
        """
        number : float
            number of the node
        df_node : dataframe
            contains all th caractéristique related to the node : 
                columns : 'Nome', 'Q', 'Tipo','Etichetta'
        """
        self.confluence = confluence
        self.number = number 
        self.list_flow = []
        
        for flow_name in df_node['Nome'].unique():
            self.list_flow.append(Flow(flow_name,
                                       self.number,
                                       df_node[df_node.Nome == flow_name]))
            
        self.flow_in = 0
        
        # check the existance of subnodes:, like node number is 1 but it exist node 1.1 and 1.2 in reality
        self.subNode = []
        if len(df_node['Nodo_num'].unique())> 1:
            # it exists at least two node
            for number_node in df_node['Nodo_num'].unique():
                subnode = Node(number_node, 
                               df_node[df_node['Nodo_num'] == number_node],
                               self.confluence)
                self.subNode.append(subnode)
            

    def set_confluence(self, confluence):
        self.confluence = confluence
    
    def set_flow_in(self, flow_in):
        self.flow_in = flow_in

    def calculate_flow_in(self):
        """
        Sum all the flow arriving to the node
        """
        self.flow_in = 0
        self.list_flow_in = []
        
        for flow in self.list_flow :
            flow.set_sign()
            
            if flow.sign > 0 :
                self.flow_in += flow.value
                self.list_flow_in.append(flow)
                
        return self.flow_in
    
    def calculate_flow_out(self):
        """
        Sum all the flow leaving the node
        """
        self.flow_out = 0
        self.list_flow_out = []
        
        for flow in self.list_flow :
            flow.set_sign()
            print(flow.name)
            if flow.sign > 0 and flow.tipo != 'Res' : 
                self.flow_out += flow.value
                self.list_flow_out.append(flow)
                
        return self.flow_out
                
    def calculate_flow_res(self):
        
        return
    
# # --------------------------- class Flow ------------------------------------        
class Flow():   
    def __init__(self, name, number, df_node):
        self.name = name
        self.node_parents = number
        self.value =  df_node['Q'].values[0]
        self.tipo = df_node['Tipo'].values[0]
        self.sign = 1

        return
   
    def set_sign(self):
       if self.tipo in ['DMV','Inflitrazione', 'Presa']:
           self.sign = -1
            
       return 
        

            

# %%

def find_confluence(df_section_rivers):
    """
    find all the node which are at a confluence
    
    Parameters : 
    ----------------
    df_section_rivers : dataframe
        columns : Tratto, flow (Q), river name
        
    Returns
    ----------------
    node_confluence : list
        all nodes which are a confluence
    """
    dict_ending_node = {}
    node_confluence = []
    
    for section_name in df_section_rivers['Tratto'].tolist():
        df_river = df_section_rivers[df_section_rivers['Tratto'] == section_name]
        river = df_river['River'].values[0]
        
        section = Section(river,df_river)
        ending_node = section.ending_number
        # check if the ending node already exits. If it does, it means there is a confluence
        if ending_node in dict_ending_node.values():
            node_confluence.append(ending_node)
        dict_ending_node[section_name] = ending_node
        
    return node_confluence


def create_river(df_section_rivers):
    """
    create all the river related to df_section_rivers
    take into account the confluence
    if at start there is two river and 1 confluence 
    we will have in output 3 rivers, the tributary the main river before and 
    after the confluence
    
    Parameter
    ------------
    df_section_rivers : dataframe
        contains data concerning rivers
    
    Returns
    ------------
    list_river : list of class
        give all the river related to df_section_rivers
    
    """
    # first find all the confluence
    node_confluence = find_confluence(df_section_rivers)
    
    # create a waiting list for all the river
    queue_river_name =  collections.deque(df_section_rivers['River'].unique())
    
    list_river = []
    
    # while there is river to treat :
    while  queue_river_name :
        # get one river from the waiting list and drop it
        river_name = queue_river_name.popleft()
        
        # create the river
        river = River(river_name, 
                      df_section_rivers[df_section_rivers['River'] == river_name])
        
        # check if there isn't a confluence in this river
        for node in node_confluence:
             if node in river.list_node_number[1:-2] : 
                 # suppress the starting and the ending node, 
                 # because at those place there is no confluence
                 [river_am, river] = river.split_river(node)
                 list_river.append(river_am)
                 
        list_river.append(river)
        
    return list_river 

            
    
    
    

# %% Test the classes
if __name__ == '__main__':    
    
    # # --------------------------test the class-------------------------------
    
    #---------------------
    # test the node classs
    number = 1.1    
    df_node_0 = df_node[df_node.Nodo_num == number]
    
    node_0_1 = Node(number, df_node_0)
    flow_in = node_0_1.calculate_flow_in()
    
    
    
    #---------------------
    # Test the section class
    river_gesso = 'gesso'
    section = '0-1'
    section_0_1 = Section(river_gesso, df_gesso[df_gesso.Tratto == section])
    
    section_0_1.create_starting_node(df_node)
    section_0_1.create_ending_node(df_node)  
    
    section_0_1.calculate_section_flow()
    #---------------------
    # Test the river class
#    df_river =  df_gesso
#    river_g = River(river_gesso, df_gesso)
    
    #---------------------
    # # ------------------------- test the function ---------------------------
#    confluence = find_confluence(df_section_rivers)
#    node_list = create_all_node(df_node,df_section_rivers)
#    list_rivers = create_river(df_section_rivers)
#    
#    gesso_am = list_rivers[0]
#    section_0_1 = gesso_am.list_section[0]
#
#    gesso_am.create_Node(df_node)
#    node_list = gesso_am.list_Node