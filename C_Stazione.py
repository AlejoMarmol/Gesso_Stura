class Stazione():
    def __init__ (self,nome_str,corso_acqua_str,n_anni,Portate_medie_mensile_per_anno_M,Portata_media_mensile_storica_a):
        self.nome=nome_str
        self.corso_acqua=corso_acqua_str
        self.n_anni=n_anni
        self.Q_med_mens_M=Portate_medie_mensile_per_anno_M
        self.Q_med_mens_storica_a=Portata_media_mensile_storica_a
