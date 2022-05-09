import numpy as np
#Introducing input values

#Input values from rivers and other sources
Q_gesso=float(input('Introduca Q gesso: '))
Q_ENEL_ord=float(input('Introduca Q ENEL ord: '))
Q_ENEL_45gg=float(input('Introduca Q ENEL 45gg: '))
Q_vermenagna=float(input('Introduca Q vermenagna: '))

#Input values from infiltration
# Q_inf_gesso=float(input('Introduca Q inf gesso prima conf: '))

#Input values from DMV
DMV_gesso_Italgen = 0.33 * 1.625
DMV_gesso_conf = 0.33 * 1.625

#Input values regarding water demand
Q_BM_NuovoCanale=float(input('Introduca Q BM da Nuovo Canale: '))
Q_BM_Bealerasso=float(input('Introduca Q BM da Bealerasso: '))
Q_BM_SA=float(input('Introduca Q BM da SantAlbano: '))
Q_BM_Pozzi=float(input('Introduca Q BM da Pozzi: '))

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
    "Q Italgen Gesso idroelettrico" : 3.6
}
Q_Italgen_Gesso_eff_d=Q_Italgen_Gesso_conc_d

Q_Italgen_45gg_conc_d={
    "Q Naviglio-Vermenagna 45gg": 0.4,
    "Q Garavella 45gg":0.15,
    "Q Bealera Maestra 45gg": 2.95
}
Q_Italgen_45gg_eff_d = Q_Italgen_45gg_conc_d

Q_Italgen_Vermenagna_conc_d={
    "Q Italgen Vermenagna" : 3.3
}
Q_Italgen_Vermenagna_eff_d = Q_Italgen_Vermenagna_conc_d

#Program startsWith

#Simulation in Gesso

# DMV_gesso_Italgen=float(input('Introduca DMV gesso alla traversa Italgen: '))
Q_gesso_res=Q_gesso+Q_ENEL_ord

Q_gesso_disp=Q_gesso_res-DMV_gesso_Italgen
if Q_gesso_disp >= 0:
    pass
else:
    Q_gesso_disp = 0

#Water demand from consortia

Q_consortia_Italgen_Gesso_conc_l=[x for x in Q_consortia_Italgen_Gesso_conc_d.values()]
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
Q_consortia_Italgen_eff_totale = np.sum(Q_consortia_Italgen_eff_a)

Q_gesso_disp = Q_gesso_disp - Q_consortia_Italgen_eff_totale
Q_disp_Italgen_idro = Q_gesso_disp

if Q_disp_Italgen_idro >= Q_Italgen_Gesso_conc_d["Q Italgen Gesso idroelettrico"]:
    Q_italgen_idroelettrico = Q_Italgen_Gesso_conc_d["Q Italgen Gesso idroelettrico"]
elif (Q_disp_Italgen_idro > 0) and (Q_disp_Italgen_idro < Q_Italgen_Gesso_conc_d["Q Italgen Gesso idroelettrico"]):
    Q_italgen_idroelettrico = Q_disp_Italgen_idro
else:
    Q_italgen_idroelettrico = 0

Q_Italgen_Gesso_eff_d["Q Italgen Gesso idroelettrico"]=Q_italgen_idroelettrico
Q_gesso_disp = Q_gesso_disp - Q_italgen_idroelettrico

Q_gesso_residuo_confluenza = Q_gesso_disp + DMV_gesso_conf

#ENEL 45gg

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
Q_Italgen_45gg_eff_totale = np.sum(Q_Italgen_45gg_eff_a)



#VERMENAGNA













