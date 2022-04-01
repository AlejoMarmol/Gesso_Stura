import pandas as pd
import numpy as np
from f_pulizia_dati import pulizia_dati
from C_Stazione import Stazione

stazioni_stura_l=["vinadio","gaiola","fossano"]
stazioni_gesso_l=["andonno"]
stazioni_vermenagna_l=["robilante"]

stazioni_gg_d=pulizia_dati()

def portate_stazioni(stazioni_gg_d):
    Stazioni_l=[]
    for stazione,serie_storica in stazioni_gg_d.items():
        anni=serie_storica["Data"].dt.year
        anni=list(dict.fromkeys(anni))
        n_y=serie_storica["Data"].dt.year.nunique()
        n_m=12
        Q_med_mens_l=[]

        for cont_a in anni:
            Q_anno_df=serie_storica[serie_storica["Data"].dt.year == cont_a]
            Q_med_mens_a_l=[]
            for cont_m in range(1,n_m+1):
                Q_mens_df=Q_anno_df[Q_anno_df["Data"].dt.month == cont_m]
                Q_med_mens=Q_mens_df["Q(m3/s)"].mean(skipna=True)
                Q_med_mens_a_l.append(Q_med_mens)
            Q_med_mens_l.append(Q_med_mens_a_l)
            Q_med_mens_M=np.array(Q_med_mens_l)
            Q_med_mens_storica_a=np.nanmean(Q_med_mens_M, axis=0)

        if stazione in stazioni_stura_l:
            Stazioni_l.append(Stazione(stazione,"Stura",n_y,Q_med_mens_M,Q_med_mens_storica_a))
        elif stazione in stazioni_gesso_l:
            Stazioni_l.append(Stazione(stazione,"Gesso",n_y,Q_med_mens_M,Q_med_mens_storica_a))
        else:
            Stazioni_l.append(Stazione(stazione,"Vermenagna",n_y,Q_med_mens_M,Q_med_mens_storica_a))

    return(Stazioni_l)