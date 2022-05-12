import pandas as pd
import numpy as np

#Input values from rivers and other sources

#Q_gesso=float(input('Introduca Q gesso: '))
#Q_ENEL_ord=float(input('Introduca Q ENEL ord: '))
#Q_ENEL_45gg=float(input('Introduca Q ENEL 45gg: '))
#Q_vermenagna=float(input('Introduca Q vermenagna: '))

Q_gesso=2.0
Q_ENEL_ord=2.0
Q_ENEL_45gg=0.0
Q_vermenagna=3.0

Q_eden = 0.4
Q_dep = 0.0

#Input values from infiltration
# Q_inf_gesso=float(input('Introduca Q inf gesso prima conf: '))
Q_inf_1 = 0.8
Q_inf_2 = 1.3
#????

#Input values from DMV
DMV_gesso_Italgen = 1 * 1.625
DMV_gesso_conf = 1 * 1.625

DMV_vermenagna_Italgen = 1 * 0.623
DMV_vermenagna_conf = 1 * 0.623

DMV_gesso_valle_confluenza = 1 * 3.057

DMV_gesso_conf_stura = 1 * 4.762




#Input values regarding water demand
#Q_BM_NuovoCanale=float(input('Introduca Q BM da Nuovo Canale: '))
#Q_BM_Bealerasso=float(input('Introduca Q BM da Bealerasso: '))
#Q_BM_Sa=float(input('Introduca Q BM da SantAlbano: '))
#Q_BM_Pozzi=float(input('Introduca Q BM da Pozzi: '))

Q_BM_NuovoCanale=1.20
Q_BM_Bealerasso=0.05
Q_BM_Sa=0.4
Q_BM_Pozzi=1.40

#Authorized flowrates
Q_consortia_Italgen_Gesso_conc_d={
    "Q Naviglio":2.70, 
    "Q Bedale": 0.30, 
    "Q Madonna Bruna":0.15,
    "Q Bealera Nuova":0.5,
    "Q Bealera Grossa e Pravero":1.80,
    "Q Piattonea e David": 0.20,
    "Q Gerbina": 0.10
    }
Q_consortia_Italgen_Gesso_eff_d = Q_consortia_Italgen_Gesso_conc_d

Q_Italgen_Gesso_conc_d={
    "Q Italgen Gesso idroelettrico" : 3.60
}
Q_Italgen_Gesso_eff_d=Q_Italgen_Gesso_conc_d

Q_Italgen_45gg_conc_d={
    "Q Naviglio-Vermenagna 45gg": 0.4,
    "Q Garavella 45gg":0.15,
    "Q Bealera Maestra 45gg": 2.95
}
Q_Italgen_45gg_eff_d = Q_Italgen_45gg_conc_d

Q_Italgen_Vermenagna_conc_d={
    "Q Italgen Vermenagna" : 3.30
}
Q_Italgen_Vermenagna_eff_d = Q_Italgen_Vermenagna_conc_d

Q_Preve_Vermenagna_conc_d={
    "Q Preve" : 0.01
}
Q_Preve_Vermenagna_eff_d = Q_Preve_Vermenagna_conc_d

Q_Nav_Ver_conc_d={
    "Q Naviglio" : 2.7,
    "Q Vermenagna" : 2.5
}
Q_Nav_Ver_eff_d = Q_Nav_Ver_conc_d

Q_g_valle_gesso_conc_d={
    "Q Lupa" : 0.3,
    "Q Lupotto DolceResiga" : 0.5,
    "Q Bollera" : 0.5,
    "Q ZappaBecchera": 0.15
}
Q_g_valle_gesso_eff_d = Q_g_valle_gesso_conc_d

Q_Bealera_Maestra_conc_d={
    "Q BM Gesso_Stura" : 6,
}
Q_Bealera_Maestra_eff_d = Q_Bealera_Maestra_conc_d

Q_Bealera_Maestra_complessiva_conc_d={
    "Q BM Gesso_Stura" : 6,
    "Q BM Nuovo Canale" : Q_BM_NuovoCanale,
    "Q BM Bealerasso" : Q_BM_Bealerasso,
    "Q BM SA" : Q_BM_Sa,
    "Q BM Pozzi": Q_BM_Pozzi
}
Q_Bealera_Maestra_complessiva_eff_d = Q_Bealera_Maestra_complessiva_conc_d


####Variabili per nodi
Q_Gesso = Q_gesso
Q_Vermenagna = Q_vermenagna
DMV_nodo_1 = DMV_gesso_Italgen
DMV_nodo_4 = DMV_vermenagna_Italgen
Q_Scarico_ENEL = Q_ENEL_ord
Q_Scarico_ENEL_45gg = Q_ENEL_45gg




#Program startsWith

#Simulation in Gesso

# DMV_gesso_Italgen=float(input('Introduca DMV gesso alla traversa Italgen: '))
Q_gesso_res=Q_gesso+Q_ENEL_ord

Q_gesso_disp=Q_gesso_res-DMV_gesso_Italgen
if Q_gesso_disp >= 0:
    pass
else:
    Q_gesso_disp = 0

Q_disp_nodo_1 = Q_gesso_disp

#Water demand from consortia

#LOOK FOR METHDOS TO CONVERT DICT INTO LIST COMMAND: .to_list()
Q_consortia_Italgen_Gesso_conc_l=[x for x in Q_consortia_Italgen_Gesso_conc_d.values()]
#ALTERNATIVES: .to_array()
Q_consortia_Italgen_Gesso_conc_a=np.array(Q_consortia_Italgen_Gesso_conc_l)
Q_consortia_Italgen_Gesso_conc_totale = float(np.sum(Q_consortia_Italgen_Gesso_conc_a))

if Q_gesso_disp >= Q_consortia_Italgen_Gesso_conc_totale:
    fattore_riparto_1 = 1
elif (Q_gesso_disp < Q_consortia_Italgen_Gesso_conc_totale) and (Q_gesso_disp >= 0):
    fattore_riparto_1 = Q_gesso_disp/Q_consortia_Italgen_Gesso_conc_totale

else:
    fattore_riparto_1=0

Q_consortia_Italgen_Gesso_eff_d.update((consortium, Q * fattore_riparto_1) for consortium, Q in Q_consortia_Italgen_Gesso_eff_d.items())
Q_consortia_Italgen_eff_l = [x for x in Q_consortia_Italgen_Gesso_eff_d.values()]
Q_consortia_Italgen_eff_a = np.array(Q_consortia_Italgen_eff_l)
Q_consortia_Italgen_eff_totale = float(np.sum(Q_consortia_Italgen_eff_a))

Q_Italgen_irr = Q_consortia_Italgen_Gesso_eff_d["Q Naviglio"] + Q_consortia_Italgen_Gesso_eff_d["Q Bedale"]

Q_gesso_disp = Q_gesso_disp - Q_consortia_Italgen_eff_totale
Q_disp_Italgen_idro = Q_gesso_disp

if Q_disp_Italgen_idro >= Q_Italgen_Gesso_conc_d["Q Italgen Gesso idroelettrico"]:
    Q_italgen_idroelettrico = Q_Italgen_Gesso_conc_d["Q Italgen Gesso idroelettrico"]
elif (Q_disp_Italgen_idro > 0) and (Q_disp_Italgen_idro < Q_Italgen_Gesso_conc_d["Q Italgen Gesso idroelettrico"]):
    Q_italgen_idroelettrico = Q_disp_Italgen_idro
else:
    Q_italgen_idroelettrico = 0

Q_Italgen_Gesso_eff_d["Q Italgen Gesso idroelettrico"]=Q_italgen_idroelettrico
Q_Italgen_Gesso_idro = Q_italgen_idroelettrico

Q_Madonna_Bruna = Q_consortia_Italgen_Gesso_eff_d["Q Madonna Bruna"]

Q_res_nodo_1 = Q_disp_nodo_1 - Q_Italgen_irr - Q_Italgen_Gesso_idro - Q_Madonna_Bruna + DMV_gesso_Italgen
Q_disp_nodo_2 = Q_res_nodo_1 - DMV_gesso_Italgen
Q_res_nodo_2 = Q_disp_nodo_2 + DMV_gesso_Italgen
Q_disp_nodo_3 = Q_res_nodo_2 - DMV_gesso_Italgen
Q_Sinistra_Gesso = Q_consortia_Italgen_Gesso_eff_d["Q Bealera Nuova"] + Q_consortia_Italgen_Gesso_eff_d["Q Bealera Grossa e Pravero"] + Q_consortia_Italgen_Gesso_eff_d["Q Piattonea e David"] + Q_consortia_Italgen_Gesso_eff_d["Q Gerbina"]
Q_res_nodo_3 = Q_disp_nodo_3 - Q_Sinistra_Gesso + DMV_gesso_Italgen

Q_gesso_residuo_confluenza = Q_res_nodo_3


#VERMENAGNA

Q_vermenagna_disp = Q_vermenagna - DMV_vermenagna_Italgen

Q_disp_nodo_4 = Q_Vermenagna - DMV_vermenagna_Italgen

if Q_vermenagna_disp >= 0:
    pass
else:
    Q_vermenagna_disp = 0


Q_disp_Italgen_Vermenagna = Q_vermenagna_disp

if Q_disp_Italgen_Vermenagna >= Q_Italgen_Vermenagna_conc_d["Q Italgen Vermenagna"]:
    Q_italgen_vermenagna = Q_Italgen_Vermenagna_conc_d["Q Italgen Vermenagna"]
elif (Q_disp_Italgen_Vermenagna > 0) and (Q_disp_Italgen_Vermenagna < Q_Italgen_Vermenagna_conc_d["Q Italgen Vermenagna"]):
    Q_italgen_vermenagna = Q_disp_Italgen_Vermenagna
else:
    Q_italgen_vermenagna = 0

Q_Italgen_Vermenagna_eff_d["Q Italgen Vermenagna"]=Q_italgen_vermenagna
Q_Italgen_Verm = Q_italgen_vermenagna
Q_res_nodo_4 = Q_disp_nodo_4 - Q_Italgen_Verm + DMV_vermenagna_Italgen



#Preve

Q_disp_nodo_5 = Q_res_nodo_4 - DMV_vermenagna_Italgen

Q_disp_Preve = Q_disp_nodo_5

if Q_disp_Preve >= Q_Preve_Vermenagna_conc_d["Q Preve"]:
    Q_Preve = Q_Preve_Vermenagna_conc_d["Q Preve"]
elif (Q_disp_Preve > 0) and (Q_disp_Preve < Q_Preve_Vermenagna_conc_d["Q Preve"]):
    Q_Preve = Q_disp_Preve
else:
    Q_Preve = 0

Q_Preve_Vermenagna_eff_d["Q Preve"]=Q_Preve

Q_res_nodo_5 = Q_disp_nodo_5 - Q_Preve + DMV_vermenagna_Italgen

Q_vermenagna_residuo_confluenza = Q_res_nodo_5


#Italgen Tunnel

Q_Italgen_ord = Q_consortia_Italgen_Gesso_eff_d["Q Naviglio"] + Q_Italgen_Gesso_eff_d["Q Italgen Gesso idroelettrico"] + Q_Italgen_Vermenagna_eff_d["Q Italgen Vermenagna"]

#Canali Naviglio-Vermenagna
#Derivazione ordinaria


Q_disp_NV_ord = Q_Italgen_ord

Q_NV_conc = Q_Nav_Ver_conc_d["Q Naviglio"] + Q_Nav_Ver_conc_d["Q Vermenagna"]

if Q_disp_NV_ord >= Q_NV_conc:
    Q_NV_eff = Q_NV_conc
    fattore_riparto_NV = 1
    # Gs_NV = 1
elif (Q_disp_NV_ord > 0) and (Q_disp_NV_ord < Q_NV_conc):
    Q_NV_eff = Q_disp_NV_ord
    fattore_riparto_NV = Q_NV_eff/Q_NV_conc
    # Gs_NV = Q_NV_eff/Q_NV_conc
else:
    Q_NV_eff = 0
    fattore_riparto_NV = 0
    # Gs_NV = 0

Q_Nav_Ver_eff_d.update((consortium, Q * fattore_riparto_NV) for consortium, Q in Q_Nav_Ver_eff_d.items())
Q_Nav_Ver_eff_l = [x for x in Q_Nav_Ver_eff_d.values()]
Q_Nav_Ver_eff_a = np.array(Q_Nav_Ver_eff_l)
Q_Nav_Ver_eff_totale = float(np.sum(Q_Nav_Ver_eff_a))

Q_Italgen_NV_pres = Q_Nav_Ver_eff_totale

#ENEL 45gg / Italgen 45gg

Q_Italgen_45gg_conc_l=[x for x in Q_Italgen_45gg_conc_d.values()]
Q_Italgen_45gg_conc_a=np.array(Q_Italgen_45gg_conc_l)
Q_Italgen_45gg_conc_totale = float(np.sum(Q_Italgen_45gg_conc_a))

if Q_ENEL_45gg >= Q_Italgen_45gg_conc_totale:
    Q_Italgen_45gg_eff_totale = Q_Italgen_45gg_conc_totale
    fattore_riparto_2=1
elif (Q_ENEL_45gg > 0) and (Q_ENEL_45gg < Q_Italgen_45gg_conc_totale):
    Q_Italgen_45gg_eff_totale = Q_ENEL_45gg
    fattore_riparto_2=Q_ENEL_45gg/Q_Italgen_45gg_conc_totale
else:
    Q_Italgen_45gg_eff_totale=0
    fattore_riparto_2 = 0

Q_Italgen_45gg_eff_d.update((consortium, Q * fattore_riparto_2) for consortium, Q in Q_Italgen_45gg_eff_d.items())
Q_Italgen_45gg_eff_l = [x for x in Q_Italgen_45gg_eff_d.values()]
Q_Italgen_45gg_eff_a = np.array(Q_Italgen_45gg_eff_l)
Q_Italgen_45gg_eff_totale = float(np.sum(Q_Italgen_45gg_eff_a))

Q_Italgen_Gesso_1 = Q_consortia_Italgen_Gesso_eff_d["Q Naviglio"] + Q_Italgen_Gesso_eff_d["Q Italgen Gesso idroelettrico"] + Q_Italgen_45gg_eff_totale
Q_Italgen_Gesso = Q_Italgen_Gesso_1
Q_Italgen = Q_Italgen_ord + Q_Italgen_45gg_eff_totale
Q_Italgen_NV_rest = Q_Italgen

#Restituzione in gesso


Q_restituzione_italgen_gesso = Q_disp_NV_ord - Q_NV_eff
Q_Italgen_a_Gesso = Q_restituzione_italgen_gesso



#GESSO DS Confluence

Q_res_nodo_6 = Q_gesso_residuo_confluenza + Q_vermenagna_residuo_confluenza

Q_res_nodo_7 = Q_res_nodo_6 + Q_restituzione_italgen_gesso


# Q_gesso_disp = Q_gesso_res - DMV_gesso_valle_confluenza

#Nodo 8 (Gruppo valle gesso)

Q_disp_nodo_8 = Q_res_nodo_7 - Q_inf_1 + Q_eden - DMV_gesso_valle_confluenza

Q_disp_VG = Q_disp_nodo_8

Q_g_valle_gesso_conc_l=[x for x in Q_g_valle_gesso_conc_d.values()]
Q_g_valle_gesso_conc_a=np.array(Q_g_valle_gesso_conc_l)
Q_g_valle_gesso_conc_totale = float(np.sum(Q_g_valle_gesso_conc_a))
Q_VG_conc = Q_g_valle_gesso_conc_totale

print(Q_VG_conc)


if Q_disp_VG >= Q_VG_conc:
    Q_VG_eff = Q_VG_conc
    fattore_riparto_VG = 1
    # Gs_NV = 1
elif (Q_disp_VG > 0) and (Q_disp_VG < Q_VG_conc):
    Q_VG_eff = Q_disp_VG
    fattore_riparto_VG = Q_VG_eff/Q_VG_conc
    # Gs_NV = Q_NV_eff/Q_NV_conc
else:
    Q_VG_eff = 0
    fattore_riparto_VG = 0
    # Gs_NV = 0

Q_g_valle_gesso_eff_d.update((consortium, Q * fattore_riparto_VG) for consortium, Q in Q_g_valle_gesso_eff_d.items())
Q_g_valle_gesso_eff_l = [x for x in Q_g_valle_gesso_eff_d.values()]
Q_g_valle_gesso_eff_a = np.array(Q_g_valle_gesso_eff_l)
Q_g_valle_gesso_eff_totale = float(np.sum(Q_g_valle_gesso_eff_a))

Q_res_nodo_8 = Q_disp_nodo_8 - Q_g_valle_gesso_eff_totale + DMV_gesso_valle_confluenza

#Bealera Maestra

Q_disp_nodo_9 = Q_res_nodo_8- Q_inf_2 + Q_dep - DMV_gesso_conf_stura

Q_disp_BM = Q_disp_nodo_9

if Q_disp_BM >= Q_Bealera_Maestra_conc_d["Q BM Gesso_Stura"]:
    Q_BM_eff = Q_Bealera_Maestra_conc_d["Q BM Gesso_Stura"]
elif (Q_disp_BM  > 0) and (Q_disp_BM  < Q_Bealera_Maestra_conc_d["Q BM Gesso_Stura"]):
    Q_BM_eff = Q_disp_BM
else:
    Q_BM_eff = 0

Q_Bealera_Maestra_eff_d["Q BM Gesso_Stura"]=Q_BM_eff
Q_res_nodo_9 = Q_disp_nodo_9 - Q_BM_eff + DMV_gesso_conf_stura

Q_gesso_residuo_confluenza_stura = Q_res_nodo_9

fn="C:/Users/alejo/OneDrive - STUDIO PD SRL/PD 2020/01 CONSORZI IRRIGUI/02 BEALERA MAESTRA/08 CONFLUENZA GESSO STURA/x QGIS_BASI/TEMP_per_bilancio_idrico_Python/Nodi_BI_calcoli_p.shp"
layer=QgsVectorLayer(fn,'','ogr')
layer_provider=layer.dataProvider()
flds = layer.fields()
fc=layer.featureCount()


flds = layer.fields()
print(flds.names())

#Q_nodi_d = {
#    "Q Gesso" : 5.3,
#    "Q Verm" : 6
#}

Q_nodi_d = {
    "Q Gesso" : Q_Gesso,
    "Q Verm" : Q_Vermenagna,
    "DMV nodo 1" : DMV_nodo_1,
    "DMV nodo 4": DMV_nodo_4,
    "Q Scarico ENEL" : Q_Scarico_ENEL,
    "Q Scarico ENEL 45gg" : Q_Scarico_ENEL_45gg,
    "Q disp nodo 1" : Q_disp_nodo_1,
    "Q Italgen irr" : Q_Italgen_irr,
    "Q Italgen Gesso idro" : Q_Italgen_Gesso_idro,
    "Q Italgen 45 gg" : Q_Italgen_45gg_eff_totale,
    "Q Italgen Gesso 1" : Q_Italgen_Gesso_1,
    "Q res nodo 1" : Q_res_nodo_1,
    "Q disp nodo 2" : Q_disp_nodo_2,
    "Q Madonna Bruna" : Q_Madonna_Bruna,
    "Q res nodo 2" : Q_res_nodo_2,
    "Q disp nodo 3" : Q_disp_nodo_3,
    "Q Sinistra Gesso" : Q_Sinistra_Gesso,
    "Q res nodo 3" : Q_res_nodo_3,
    "DMV nodo 6 da Gesso" : DMV_gesso_conf,
    "Q disp nodo 4" : Q_disp_nodo_4,
    "Q Italgen Verm" : Q_Italgen_Verm,
    "Q Italgen Gesso" : Q_Italgen_Gesso,
    "Q Italgen" : Q_Italgen,
    "Q res nodo 4" : Q_res_nodo_4,
    "Q disp nodo 5" : Q_disp_nodo_5,
    "Q Preve" : Q_Preve,
    "Q res nodo 5" : Q_res_nodo_5,
    "DMV nodo 6 da Vermenagna" : DMV_vermenagna_conf,
    "Q Italgen Nav-Verm rest" : Q_Italgen_NV_rest,
    "Q Italgen Nav-Verm presa" : Q_Italgen_NV_pres,
    "Q Nav-Verm ord" : Q_Italgen_NV_pres,
    "Q Italgen int" : Q_Italgen_45gg_eff_totale,
    "Q Italgen in Gesso" : Q_Italgen_a_Gesso,
    "Q res nodo 6" : Q_res_nodo_6,
    "Q res nodo 7" : Q_res_nodo_7,
    "DMV nodo 7" : DMV_gesso_valle_confluenza,
    "DMV nodo 8" : DMV_gesso_valle_confluenza,
    "Q Eden Farm" : Q_eden,
    "Q inf 1" : Q_inf_1,
    "Q disp nodo 8" : Q_disp_nodo_8,
    "Q gruppo" : Q_g_valle_gesso_eff_totale,
    "Q res nodo 8" : Q_res_nodo_8,
    "DMV nodo 9" : DMV_gesso_conf_stura,
    "Q Depuratore" : Q_dep,
    "Q inf 2" : Q_inf_2,
    "Q disp nodo 9" : Q_disp_nodo_9,
    "Q Bealera Maestra" : Q_BM_eff,
    "Q res nodo 9" : Q_res_nodo_9,
}

for nodo, Q in Q_nodi_d.items():
    layer.selectByExpression("\"Nome\" = '{}'".format(nodo))
#    fids = layer.selectedFeatureIds()
    print(fids)
#    fid = fids[0]
#    print(fid)
    Qi = float(Q)
    c=layer.selectedFeatureCount()
    print(c)
    if c>0:
        fids = layer.selectedFeatureIds()
        fid=fids[0]
        print(fid)
        attrs = {flds.indexOf("Q") : Qi}
        layer_provider.changeAttributeValues({fid : attrs})

