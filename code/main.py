#!/usr/bin/python3.10

import sys
import ife.interface as intf
import reg.regexpr as r
import reg.tools as t
import reg.pnj as p

def main():
    "Procédure principale"
    ld = Loader("data/data.ini")

    # permet un affichage non-graphique
    if("-ng" in sys.argv):
        monPnj = nouveauPnj(ld)
        lst = []
        for key in monPnj.carac:
            lst.append([key.replace('_',' '),monPnj.carac[key]])
        for e in lst:
            print(f"{e[0]} = {e[1]}")
    else:
        intf.affichage(ld)
        
def nouveauPnj(ld,pnj=None,charac=None):
    return p.Pnj(ld,current=pnj,change=charac)




class NeuralPrep:
    "Contient les méthodes permettant de se mettre en lien avec le réseau de neurones"
    def cv(arg):
        # dictionnaire de fréquence
        return {
            'a':25,
            'b':11,
            'c':15,
            'd':16,
            'e':26,
            'f':8,
            'g':12,
            'h':9,
            'i':24,
            'j':4,
            'k':3,
            'l':18,
            'm':14,
            'n':22,
            'o':19,
            'p':13,
            'q':7,
            'r':21,
            's':23,
            't':20,
            'u':17,
            'v':10,
            'w':2,
            'x':5,
            'y':6,
            'z':1}[arg]

    def convert_to_ints(nom):
        nom = nom.lower()
        liste = []
        for l in nom:
            liste.append(NeuralPrep.cv(l))
        return liste

    def complet(type,texte):
        match type:
            case "closer":
                return 4 - len(texte)
            case _:
                return 2

    def completion():
        pass



class Loader:
    """Classe de chargement des datas en un dictionnaire
    TODO permettre à l'utilisateur de choisir son fichier de données
    """
    
    def __init__(self,fichier):
        """Chargement du fichier de données en un dico de listes
        le symbole dièse sera la marque d'un commentaire dans le fichier
        
        Keywords arguments
        fichier - str, adresse d'un fichier à lire
        """
        self.dict = {}
        with open(fichier,"r", encoding="utf-8") as reader:
            for l in reader:
                if(l[0]!='#'):
                    l = l[:-1]
                    a,b = l.split(":")[0],l.split(":")[1]
                    self.dict[a] = b.split(",")

# si on lance via ligne de commande, on exécute la fonction main
if __name__ == "__main__":
    main()
