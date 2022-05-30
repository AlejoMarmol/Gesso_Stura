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
# =============================================================================
# ---------------------------------- RIVER ------------------------------------
# ============================================================================= 
class River():
    # -------------------------------------------------------------------------
    def __init__(self,river, df_river, df_node):
        """
        init : 
            name of the river
            sections related to the river
            number of the node related to the river
        """
        self.name = river
        self.list_section = []
        self.list_node_number = []
        self.list_node = []
        
        # create the section of the river
        for section_name in df_river['Tratto'].unique():
            section = Section(section_name,
                              df_river[df_river.Tratto == section_name])
                
            self.list_section.append(section)
            # create the node of the section
            section.create_starting_node(df_node)
            section.create_ending_node(df_node)
            
            # add the node in the list of node of the river
            self.list_node.append(section.starting_node)
            self.list_node_number.append(section.starting_node.number)
        
        # add the last node which the ending node of the last section
        self.list_node.append(section.ending_node)
        self.list_node_number.append(section.ending_node.number)

        
    # -------------------------------------------------------------------------
    def create_copy(self):
        return copy.copy(self)
    
    # -------------------------------------------------------------------------      
    def set_river_name(self, new_name):
        self.name = new_name
        
    # -------------------------------------------------------------------------    
    def set_section_list(self, list_section):
        self.list_section = list_section
        
    # -------------------------------------------------------------------------    
    def set_node_list(self, list_node):
        self.list_node = list_node
        
    # -------------------------------------------------------------------------
    def set_node_number_list(self, list_node_number):
        self.list_node_number = list_node_number
                    
    # -------------------------------------------------------------------------
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
            
            # ------------------ create the downstream river ------------------
            River_av = self.create_copy()
            # set the river name
            River_av.set_river_name(self.name + '_av')
            # set the section list
            River_av.set_section_list(self.list_section[index_split:])
            # set the node list
            River_av.set_node_list(self.list_node[index_split:])
            # set the node number list
            River_av.set_node_number_list(self.list_node_number[index_split:])
            
            # ------------------ create the upstream river --------------------
            self.set_river_name(self.name + '_am')
            # set the section list
            self.set_section_list(self.list_section[:index_split])
            # set the node list
            self.set_node_list(self.list_node[:index_split] + [self.list_node[index_split]])
            # set the node number list 
            list_node_number = self.list_node_number[:index_split]+ [self.list_node_number[index_split]]
            self.set_node_number_list(list_node_number)
            
            return [self, River_av]
        
    # ------------------------------------------------------------------------- 
    def _flow_presa(self):
        """
        Calculate all the flow need for the presa inside 
        """
         
        self.flow_presa = 0
        for node in self.list_node:
            presa = node.get_tipo_value('Presa')
            self.flow_presa += presa
        
        return self.flow_presa
    
            
# %%
# =============================================================================
# --------------------------------- SECTION -----------------------------------
# =============================================================================
class Section():
    # -------------------------------------------------------------------------
    def __init__(self, river,  df_river, flow=None):
        self.river = river
        self.tratto = df_river['Tratto'].values[0]
        
        if flow == None:
            self.flow = df_river['Q'].values[0]
        else : 
            self.flow = flow
        
        # nodes related to the section, the information is contained in the "
        # tratto : 0-1 means starting node = 0 , and ending node = 1"
        list_node = self.tratto.split('-')
        self.starting_number = int(list_node[0])
        self.ending_number = int(list_node[1])
        
    # -------------------------------------------------------------------------            
    def create_starting_node(self, df_node):
        """
        Create the Node class associated to the starting node of the section
        
        Parameters
        -------------
        df_node : dataframe
            
        """
        self.starting_node = Node(self.starting_number,
                                df_node[df_node['Nodo_num'].astype(int) == self.starting_number])

    # -------------------------------------------------------------------------                
    def create_ending_node(self, df_node):
        """
        Create the Node class associated to the ending node of the section
        
        Parameters
        -------------
        df_node : dataframe
            
        """
        self.ending_node = Node(self.ending_number,
                                df_node[df_node['Nodo_num'].astype(int) == self.ending_number])
        

    # -------------------------------------------------------------------------                
    def calculate_section_flow(self):
        """
        calculate the section flow based on the flow leaving of the starting node
        In the mean time set the flow coming at the ending_node
        """
#        if self.starting_Node.subNode  :
#            self.flow_section = self.starting_Node.subNode[-1].calculate_section_out()
#        else:
        self.flow_section = self.starting_node.calculate_section_out()
        
#        if self.ending_Node.subNode  :
#            self.ending_Node.subNode[0].add_flow_section(self.flow_section)
#        else :
        self.ending_node.add_flow_section(self.flow_section)
        
        return self.flow_section
    
 
# %%           
# =============================================================================
# ----------------------------------- NODE ------------------------------------
# =============================================================================
class Node():
    # -------------------------------------------------------------------------
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
        self.list_flow_name = df_node['Nome'].unique().tolist()
        self.list_flow_tipo = df_node['Tipo'].unique().tolist()
        self.list_flow = []
        
        for flow_name in self.list_flow_name :
            flow = Flow(flow_name,
                        self.number,
                        df_node[df_node.Nome == flow_name])

            self.list_flow.append(flow)
        
        # set the input flow based on the value of the input flow, whithout the section flow
        self.flow_in = self.get_tipo_value('Input') + self.get_tipo_value('Restitution')
        
        # check the existance of subnodes:, like node number is 1 but it exist node 1.1 and 1.2 in reality
        self.subNode = []
        if len(df_node['Nodo_num'].unique())> 1:
            # it exists at least two node
            for number_node in df_node['Nodo_num'].unique():
                subnode = Node(number_node, 
                               df_node[df_node['Nodo_num'] == number_node],
                               self.confluence)
                self.subNode.append(subnode)
            
    # -------------------------------------------------------------------------   
    def set_confluence(self, confluence):
        self.confluence = confluence
        
    # -------------------------------------------------------------------------    
    def get_tipo_value(self, flow_tipo):
        """
        get the value of a specific flow belonging at the node
        if it doesn't exist for the node, return an error
        
        Parameter
        --------------
        flow_name : string
            name of the flow from which we want it value
            
        Return
        --------------
        flow.value : float
             value of the flow_name
        """
        flow_value = 0 # the 0 value all to get a value even if the flow  doesn't exist
        for flow in self.list_flow : # have to look all the list in case the tipo exist twice or more

            if flow.tipo == flow_tipo:
                flow_value = flow_value + flow.value
                
        return(flow_value)
        
    # -------------------------------------------------------------------------
    def set_tipo_value(self, flow_tipo, flow_value):
        """
        set the value of a specific tipo belonging to the node
        if it doesn't exist for the node, return an error
        
        Nota : If there is at least two flow with the same tipo, 
        use set_flow_name_value
        
        Parameter
        --------------
        flow_tipo : string
            name of the flow's tipo from which we want it value
        
        flow_value : float
            value of the flow
            
        Return
        --------------
        """
        if flow_tipo in self.list_flow_tipo :
            index_flow = self.list_flow_tipo.index(flow_tipo)
            flow =  self.list_flow[index_flow]
            flow.value = flow_value
                
        else :
            print(' Attention the flow : ' + flow_tipo +  ', does not exist for the node : '+ str(self.number))
            return 
    
    # -------------------------------------------------------------------------
    def set_flow_name_value(self, flow_name, flow_value):
        """
        set the value of a specific flow name belonging to the node
        if it doesn't exist for the node, return an error
        
        Parameter
        --------------
        flow_name : string
            name of the flow from which we want it value
            
        flow.value : float
             value of the flow_name
        """
        if flow_name in self.list_flow_name :
            index_flow = self.list_flow_name.index(flow_name)
            flow =  self.list_flow[index_flow]
            flow.value = flow_value
                
        else :
            print(' Attention the flow : ' + flow_name +  ', does not exist for the node : '+ str(self.number))
            return
    # -------------------------------------------------------------------------
    def add_flow_section(self, flow_in):
        """
        the flow coming to a node is the flow of the section + the flow of all inputs
        """
        self.flow_in = flow_in + self.flow_in
        
    # -------------------------------------------------------------------------    
    def set_flow_disp(self):
        """
        set the value of the available flow inside the river
        
        Return
        ---------
        flow_disp : float
            Value of the available flow
        """
        # get the value of DMW
        flow_DMV  = self.get_tipo_value('DMV')
        
        # calculate the flow available
        flow_Disp = self.flow_in - flow_DMV
        
        # set the true value, if flow_Disp <0, then flow_Disp == 0
        if flow_Disp > 0 : 
            self.set_tipo_value('Disp', flow_Disp)
            return flow_Disp
        else :
            self.set_tipo_value('Disp', 0)
            return 0
            
    # -------------------------------------------------------------------------        
    def set_flow_res(self, flow_presa):
        """
        set the value of the restitution flow
        """
        # get the value of the output flow due to inflitrazion
        # ... in coming
        # 
        if 'Res' in self.list_flow_tipo : 
            flow_disp = self.set_flow_disp() 
            flow_res = flow_disp - flow_presa
        
            # set the value of res
            self.set_tipo_value( 'Res', flow_res)
        
            return flow_res
        
        else:
            return('the flow : Res, does not exist for the node'+ self.number)
            
    # ------------------------------------------------------------------------- 
    def set_flow_output(self):
        """
        set the value of an output
        """
        self.flow_output_presa = 0
        if 'Output' in self.list_flow_tipo : 
            self.flow_output_presa = self.get_tipo_value('Presa')
        return self.flow_output_presa
            
   
    # -------------------------------------------------------------------------
    def calculate_section_out(self):
        """
        get the flow which is realized into the river after the node
        """
        # calculate the flow going into the river
        flow_presa = self.get_tipo_value('Presa')
        flow_inflitrazion = self.get_tipo_value('Inflitration')
        self.flow_out = flow_presa + flow_inflitrazion
        
                
        # calculate the flow available  
        flow_Disp = self.set_flow_disp()
        print(flow_Disp)
        # set the value
        section_out = flow_Disp - self.flow_out
        if section_out > 0 :
            return section_out
        else :
            
            return 0


# %%  
# =============================================================================
# ----------------------------------- FLOW ------------------------------------
# =============================================================================       
class Flow():   
    # -------------------------------------------------------------------------
    def __init__(self, name, number, df_node):
        self.name = name
        self.node_parents = number
        self.value =  df_node['Q'].values[0]
        self.tipo = df_node['Tipo'].values[0]
        self.sign = 1

        return
    # -------------------------------------------------------------------------
    def set_sign(self):
       if self.tipo in ['Inflitrazione', 'Presa','Res']:
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


def create_river(df_section_rivers, df_node):
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
                      df_section_rivers[df_section_rivers['River'] == river_name],
                      df_node)
        
        # check if there isn't a confluence in this river
        for confluence_number in node_confluence:
             if confluence_number in river.list_node_number[1:-2] : 
                 # suppress the starting and the ending node, 
                 # because at those place there is no confluence
                 [river_am, river] = river.split_river(confluence_number)
                 list_river.append(river_am)
                 
        list_river.append(river)
        
    return list_river 

            
    
    
    

# %% Test the classes
if __name__ == '__main__':    
    
    # # --------------------------test the class-------------------------------
    
    #---------------------
    # test the node classs
    print(' Test Node class')
    number = 1.1    
    df_node_0 = df_node[df_node.Nodo_num == number]
    
    node_0_1 = Node(number, df_node_0)
    node_0_1.get_tipo_value('DMV')
    
    
    #---------------------
    # Test the section class
    print('***********')
    print(' Test Section class')
    river_gesso = 'gesso'
    section = '0-1'
    section_0_1 = Section(river_gesso, df_gesso[df_gesso.Tratto == section])
    
    section_0_1.create_starting_node(df_node)
    section_0_1.create_ending_node(df_node)  
    
    section_0_1.calculate_section_flow()
    #---------------------
    # Test the river class
#    print('***********')
#    print(' Test Section class')
#    
#    df_river =  df_gesso
#    river_g = River(river_gesso, df_gesso, df_node)
    
    
    #---------------------
    # # ------------------------- test the function ---------------------------
    confluence = find_confluence(df_section_rivers)
    list_rivers = create_river(df_section_rivers, df_node)
    
    gesso_am = list_rivers[0]
    section_0_1 = gesso_am.list_section[0]
    node_1 = gesso_am.list_node[1]
    node_1_1 = node_1.subNode[1]