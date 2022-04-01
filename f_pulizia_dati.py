import pandas as pd

def pulizia_dati():

    stura_vinadio_gg_df=pd.read_csv("dati_stazioni/VINADIO STURA DI DEMONTE_giornalieri_2008_2020.csv", sep=";")
    stura_gaiola_gg_df=pd.read_csv("dati_stazioni/GAIOLA STURA DI DEMONTE_giornalieri_2003_2020.csv", sep=";")
    stura_fossano_gg_df=pd.read_csv("dati_stazioni/FOSSANO STURA DI DEMONTE_giornalieri_2000_2020.csv", sep=";")   
    gesso_andonno_gg_df=pd.read_csv("dati_stazioni/ANDONNO GESSO_giornalieri_2008_2020.csv", sep=";")
    vermenagna_robilante_gg_df=pd.read_csv("dati_stazioni/ROBILANTE VERMENAGNA_giornalieri_2008_2020.csv", sep=";")

    stazioni_originali_d={
        "vinadio":stura_vinadio_gg_df,
        "gaiola":stura_gaiola_gg_df,
        "fossano":stura_fossano_gg_df,
        "andonno":gesso_andonno_gg_df,
        "robilante":vermenagna_robilante_gg_df}
    stazioni_pulite_d={}


    for stazione,serie_storica in stazioni_originali_d.items():
        serie_storica.drop(columns="Unnamed: 3", inplace=True)
        serie_storica.rename(columns={"Portata fiume ( mc/s )":"Q(m3/s)","Livello idrometrico fiume ( m )":"h(m)"}, inplace=True)
        serie_storica["Q(m3/s)"]=serie_storica["Q(m3/s)"].str.replace(',','.')
        serie_storica["h(m)"]=serie_storica["h(m)"].str.replace(',','.')
        serie_storica["Q(m3/s)"]=serie_storica["Q(m3/s)"].astype(float)
        serie_storica["h(m)"]=serie_storica["h(m)"].astype(float)
        serie_storica['Data']=pd.to_datetime(serie_storica['Data'],format="%d/%m/%Y")
        stazioni_pulite_d[stazione]=serie_storica
    
    return(stazioni_pulite_d)

