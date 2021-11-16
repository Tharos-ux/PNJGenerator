#!/usr/bin/python   
print('Content-type: text/html\r\n\r')

import random
import numpy as np
import tkinter

def main():
    "Procédure principale"
    ld = Loader("data.ini")

    monPnj = Pnj(ld)

    # Linéarisation de la donnée

    lst = []

    for key in monPnj.carac:
        lst.append([key,monPnj.carac[key]])
   
    print(lst)

class Tools:
    "Contient des méthodes de calcul et de génération"

    def loi_normale(mu, sigma):
        "Renvoie le premier entier strictement positif généré selon une loi normale."
        n = 0
        while (n<=0):
            n = np.random.randn(1) * sigma + mu
        return int(n[0])

    def gen_nom(sexe,ld):
        "Sexe doit être au format M ou F"
        opener,closer,mid1,mid2,a = random.choice(ld.dict["Opener"]),random.choice(ld.dict["Closer"+sexe[0]]),random.choice(ld.dict["Middle"]),random.choice(ld.dict["Middle"]),random.randrange(3)
        if(a==0): return opener+mid1+mid2+closer
        elif(a==1): return opener+closer+mid1+closer
        else: return opener+closer

    def fill(ld,sexe,nom,age):
        "Effectue une attribution des caractéristiques annexes"
        blacklist = ["Opener","CloserM","CloserF","Middle"]
        dico = {'Nom' : nom,'Age' : age, 'Sexe biologique' : sexe}
        for key in ld.dict:
            if(key not in blacklist):
                if(key[0]=='%'):
                    # on doit sélectionner selon une probabilité
                    probas,valeurs = [],[]
                    for e in ld.dict[key]:
                        probas.append(e.split('%')[0])
                        valeurs.append(e.split('%')[1])
                    dico[key[1:]] = np.random.choice(valeurs,1,probas)[0]
                elif(key[0]=='|'):
                    # caractère chainé en fonction d'une autre caractéristique
                    test,cle = key.split('~')[0],key.split('~')[1]
                    filtre,val,comparateur = test.split(' ')[0][1:],test.split(' ')[2],test.split(' ')[1]
                    if(filtre in dico.keys()):
                        if(comparateur=="=="):
                            if(dico[filtre]==val): dico[cle] = random.choice(ld.dict[key])
                        if(comparateur==">="):
                            if(int(dico[filtre])>=int(val)): dico[cle] = random.choice(ld.dict[key])
                        if(comparateur=="<="):
                            if(int(dico[filtre])<=int(val)): dico[cle] = random.choice(ld.dict[key])
                else:
                    # sélection aléatoire basique
                    dico[key] = random.choice(ld.dict[key])
        return dico

class Pnj:
    "Contient les méthodes permettant de créer un objet PnJ"

    def __init__(self,ld):
        "Initialise un nouvel objet PnJ"
        self.sexe = "Féminin" if(random.randrange(2)==0) else "Masculin"
        self.name = Tools.gen_nom(self.sexe,ld)
        self.age = Tools.loi_normale(30,20)
        self.carac = Tools.fill(ld,self.sexe,self.name,self.age)

    def __str__(self):
        "Renvoie une description du PnJ"
        return f"{self.name} est âgé de {self.age} ans."

class Loader:
    "Classe de chargement des datas en un dictionnaire"
    
    def __init__(self,fichier):
        "Chargement du fichier de données en un dico de listes"
        self.dict = {}
        with open(fichier,"r") as reader:
            for l in reader:
                if(l[0]!='#'): # le symbole dièse sera la marque d'un commetaire dans le fichier
                    l = l[:-1]
                    a,b = l.split(":")[0],l.split(":")[1]
                    self.dict[a] = b.split(",")

# si on lance via ligne de commande, on exécute la fonction main
if __name__ == "__main__":
    main()
