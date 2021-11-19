#!/usr/bin/python3.10

import random
#import numpy as np
import tkinter
import sys
import interface

def main():
    "Procédure principale"
    ld = Loader("data.ini")

    # permet un affichage non-graphique
    if("-ng" in sys.argv):
        monPnj = nouveauPnj(ld)
        lst = []
        for key in monPnj.carac:
            lst.append([key.replace('_',' '),monPnj.carac[key]])
        for e in lst:
            print(f"{e[0]} = {e[1]}")
    else:
        interface.affichage(ld)
        
def nouveauPnj(ld):
    return Pnj(ld)

def conversion(string):
    # quand on arrive ici, on considère que la chaine est chainée
    #ischained = ('|' in string)
    #isproba = ('%' in string)
    string = string.replace('|','').replace('%','') # on supprime les tags
    islogical = ('&' in string) or ('$' in string)
    hasparenthesis = ('(' in string) or (')' in string)
    match [islogical,hasparenthesis]:
        case [_,False]:
            liste = string.split(' ')
            return conv(liste) # lecture gauche à droite, pas de prio opératoire
        case [True,True]:
            pass # pour le moment on gère pas des parenthèses

def conv(liste):
    if(len(liste)>3):
        if(liste[3]=='&'): return Regexpr.And(Regexpr.Element(liste[0],liste[1],liste[2]),conv(liste[4:]))
        if(liste[3]=='$'): return Regexpr.Or(Regexpr.Element(liste[0],liste[1],liste[2]),conv(liste[4:]))
    else:
        return Regexpr.Element(liste[0],liste[1],liste[2])

class Tools:
    "Contient des méthodes de calcul et de génération"

    def loi_normale(mu, sigma):
        "Renvoie le premier entier strictement positif généré selon une loi normale."
        n = 0
        while (n<=0):
            n = random.random() * sigma + mu
        return int(n)

    def weighted_choice(keys,probas):
        "Sélectionne une clé en fonction d'un poids de probabilité"
        cumulatedProbas,summ = [],0
        for e in probas:
            cumulatedProbas.append(e+summ)
            summ+=e
        maximum = cumulatedProbas[-1]
        select = random.randint(0,maximum)
        i = 0
        while i<len(probas):
            if (cumulatedProbas[i] > select): return keys[i]
            i+=1 # retourne la première occurence d'un nombre inférieur
        return keys[-1] # ou la dernière occurence de la liste sinon

    def gen_nom(sexe,ld):
        "Sexe biologique doit être au format Masculin ou Féminin"
        opener,closer,mid1,mid2,a = random.choice(ld.dict["Opener"]),random.choice(ld.dict["Closer"+sexe[0]]),random.choice(ld.dict["Middle"]),random.choice(ld.dict["Middle"]),random.randrange(3)
        if(a==0): return opener+mid1+mid2+closer
        elif(a==1): return opener+closer+mid1+closer
        else: return opener+closer

    def fill_regexpr(ld,sexe,nom,age):
        "Effectue une attribution des caractéristiques annexes"
        blacklist = ["Opener","CloserM","CloserF","Middle"]
        dico = {'Nom' : nom,'Age' : age, 'Sexe_biologique' : sexe}
        for key in ld.dict:
            if(key not in blacklist):
                if('%' in key):
                    if('|' in key):
                        probas,valeurs = [],[]
                        for e in ld.dict[key]:
                            probas.append(int(e.split('%')[0]))
                            valeurs.append(e.split('%')[1])
                        # caractère chainé en fonction d'une autre caractéristique + proba
                        # print(f"PROBAS {probas} > VALEURS : {valeurs}")
                        test,cle = key.split('~')[0],key.split('~')[1]
                        if(Regexpr.res(conversion(test),dico)): dico[cle] = Tools.weighted_choice(valeurs,probas)
                    else:
                        # on doit sélectionner selon une probabilité simple
                        probas,valeurs = [],[]
                        for e in ld.dict[key]:
                            probas.append(int(e.split('%')[0]))
                            valeurs.append(e.split('%')[1])
                        dico[key[1:]] = Tools.weighted_choice(valeurs,probas)
                elif(key[0]=='|'):
                    # caractère chainé en fonction d'une autre caractéristique
                    test,cle = key.split('~')[0],key.split('~')[1]
                    if(Regexpr.res(conversion(test),dico)): dico[cle] = random.choice(ld.dict[key])
                else:
                    # sélection aléatoire basique
                    dico[key] = random.choice(ld.dict[key])
        return dico

    def fill(ld,sexe,nom,age):
        "Effectue une attribution des caractéristiques annexes"
        blacklist = ["Opener","CloserM","CloserF","Middle"]
        dico = {'Nom' : nom,'Age' : age, 'Sexe_biologique' : sexe}
        for key in ld.dict:
            if(key not in blacklist):
                if(key[0]=='%'):
                    if(key[1]=='|'):
                        probas,valeurs = [],[]
                        for e in ld.dict[key]:
                            probas.append(int(e.split('%')[0]))
                            valeurs.append(e.split('%')[1])
                        # caractère chainé en fonction d'une autre caractéristique + proba
                        # print(f"PROBAS {probas} > VALEURS : {valeurs}")
                        test,cle = key.split('~')[0],key.split('~')[1]
                        filtre,val,comparateur = test.split(' ')[0][2:],test.split(' ')[2],test.split(' ')[1]
                        if(filtre in dico.keys()):
                            if(comparateur=="==" and dico[filtre]==val[1:-1]) or (comparateur=="!=" and dico[filtre]!=val[1:-1]) or (comparateur==">=" and int(dico[filtre])>=int(val)) or (comparateur=="<=" and int(dico[filtre])<=int(val)): dico[cle] = Tools.weighted_choice(valeurs,probas)
                    else:
                        # on doit sélectionner selon une probabilité simple
                        probas,valeurs = [],[]
                        for e in ld.dict[key]:
                            probas.append(int(e.split('%')[0]))
                            valeurs.append(e.split('%')[1])
                        dico[key[1:]] = Tools.weighted_choice(valeurs,probas)
                elif(key[0]=='|'):
                    # caractère chainé en fonction d'une autre caractéristique
                    test,cle = key.split('~')[0],key.split('~')[1]
                    filtre,val,comparateur = test.split(' ')[0][1:],test.split(' ')[2],test.split(' ')[1]
                    if(filtre in dico.keys()):
                        # print(f"On compare {str(dico[filtre])} à {val[1:-1]} selon le comparateur {comparateur}. Sont-ils égaux ? {str(dico[filtre])==str(val[1:-1])}")
                        if(comparateur=="==" and dico[filtre]==val[1:-1]) or (comparateur=="!=" and dico[filtre]!=val[1:-1]) or (comparateur==">=" and int(dico[filtre])>=int(val)) or (comparateur=="<=" and int(dico[filtre])<=int(val)): dico[cle] = random.choice(ld.dict[key])
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
        self.age = Tools.loi_normale(10,10)
        self.carac = Tools.fill_regexpr(ld,self.sexe,self.name,self.age)

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

class Regexpr:
    "Modélisation d'expression régulières"

    def res(expr,dico):
        "Evaluation d'une expression régulière"
        match expr:
            case Regexpr.Or(expr1,expr2):
                return (Regexpr.res(expr1,dico) or Regexpr.res(expr2,dico))
            case Regexpr.And(expr1,expr2):
                return (Regexpr.res(expr1,dico) and Regexpr.res(expr2,dico))
            case Regexpr.Vide():
                return True
            case Regexpr.Element(cle,comparateur,valeur):
                return Regexpr.evaluate(cle,comparateur,valeur,dico)
            case True:
                return True
            case False:
                return False

    def evaluate(filtre,comparateur,val,dico):
        if(filtre in dico.keys()):
            if(comparateur=="==" and dico[filtre]==val[1:-1]) or (comparateur=="!=" and dico[filtre]!=val[1:-1]) or (comparateur==">=" and int(dico[filtre])>=int(val)) or (comparateur=="<=" and int(dico[filtre])<=int(val)):
                return True
        return False

    class Or:
        __match_args__ = ("a", "b") 
        def __init__(self,expr1,expr2):
            self.a = expr1
            self.b = expr2
        
        def __str__(self):
            return f"Or({self.a},{self.b})"

    class And:
        __match_args__ = ("a", "b") 
        def __init__(self,expr1,expr2):
            self.a = expr1
            self.b = expr2

        def __str__(self):
            return f"And({self.a},{self.b})"

    class Element:
        __match_args__ = ("a","comp","b") 
        def __init__(self,cle,comparateur,valeur):
            self.a = cle
            self.comp = comparateur
            self.b = valeur

        def __str__(self):
            return f"{self.a} {self.comp} {self.b}"

    class Vide:
        def __init__(self):
            pass
        
        def __str__(self):
            return "-empty-"


# si on lance via ligne de commande, on exécute la fonction main
if __name__ == "__main__":
    main()
