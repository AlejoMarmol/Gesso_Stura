import pandas as pd
import numpy as np

from Concessioni import Q_consortia_Italgen_Gesso_conc_d, Q_consortia_Italgen_Gesso_eff_d, Q_consortia_Sinistra_Gesso_conc_d, Q_consortia_Sinistra_Gesso_eff_d, Q_Italgen_Gesso_conc_d, Q_Italgen_45gg_conc_d, Q_Italgen_45gg_eff_d, Q_Italgen_Vermenagna_conc_d, Q_Italgen_Vermenagna_eff_d, Q_Preve_Vermenagna_conc_d, Q_Preve_Vermenagna_eff_d, Q_Nav_Ver_conc_d, Q_Nav_Ver_eff_d, Q_g_valle_gesso_conc_d, Q_g_valle_gesso_eff_d, Q_Bealera_Maestra_conc_d, Q_Bealera_Maestra_eff_d, Q_Bealera_Maestra_complessiva_conc_d, Q_Bealera_Maestra_complessiva_eff_d 
from Fabbisogni import Q_consortia_Italgen_Gesso_fab_d, Q_consortia_Italgen_Gesso_fab_eff_d, Q_Nav_Ver_fab_d, Q_Nav_Ver_fab_eff_d, Q_g_valle_gesso_fab_d, Q_g_valle_gesso_fab_eff_d, Q_Bealera_Maestra_fab_d, Q_Bealera_Maestra_fab_eff_d

from Operazioni_dizionari import dict_2_tot
##### VALORI DI INPUT

#### Fiumi e ENEL
Q_gesso=12.0
Q_ENEL_ord=3.0
Q_ENEL_45gg=0.0
Q_vermenagna=3.0

Q_res_m_nodo_1 = Q_gesso + Q_ENEL_ord

#### Restituzioni o portate in entrara
Q_eden = 0.0
Q_dep = 0.0

#### Dispersioni nel sottosuolo
Q_inf_1 = 0.8
Q_inf_2 = 1.3
Q_inf_m_conf = 0.0

#### DMV
DMV_gesso_Italgen = 1 * 1.625
DMV_gesso_conf = 1 * 1.625
DMV_vermenagna_Italgen = 1 * 0.623
DMV_vermenagna_conf = 1 * 0.623
DMV_gesso_valle_confluenza = 1 * 3.057
DMV_dx_gesso = 1 * 3.057
DMV_gesso_conf_stura = 1 * 4.762

#### Portate Bealera Maestra
Q_BM_Stura = 3.0
Q_BM_NuovoCanale=0.8
Q_BM_Bealerasso=0.05
Q_BM_Sa=0.5
Q_BM_Pozzi=1.40

#### Altri input
Q_lim_conc = 6.0

####Variabili per nodi
Q_Gesso = Q_gesso
Q_Vermenagna = Q_vermenagna
DMV_nodo_1 = DMV_gesso_Italgen
DMV_nodo_4 = DMV_vermenagna_Italgen
Q_Scarico_ENEL = Q_ENEL_ord
Q_Scarico_ENEL_45gg = Q_ENEL_45gg


##### INIZIA SIMULAZIONE

##### GESSO

Q_gesso_res=Q_res_m_nodo_1
Q_gesso_disp=Q_res_m_nodo_1-DMV_gesso_Italgen

if Q_gesso_disp >= 0:
    pass
else:
    Q_gesso_disp = 0

Q_disp_m_nodo_1 = Q_gesso_disp


Q_consortia_Sinistra_Gesso_conc_totale = dict_2_tot(Q_consortia_Sinistra_Gesso_conc_d)
