#!/usr/bin/python3.10

import random
import numpy as np
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
    elif("-old" in sys.argv):
        monPnj = nouveauPnj(ld)
        lst = []
        for key in monPnj.carac:
            lst.append([key.replace('_',' '),monPnj.carac[key]])
        total_rows = len(lst) 
        total_columns = len(lst[0])
        tableau = tkinter.Tk() 
        t = Table(tableau,total_rows,total_columns,lst) 
        tableau.mainloop()
    else:
        interface.affichage(ld)
        

def nouveauPnj(ld):
    return Pnj(ld)

class Table: 
      
    def __init__(self,root,total_rows,total_columns,lst): 
        for i in range(total_rows): 
            for j in range(total_columns): 
                  
                self.e = tkinter.Entry(root, width=24, fg='black', font=('Arial',12,'bold')) 
                  
                self.e.grid(row=i, column=j) 
                self.e.insert(tkinter.END, lst[i][j])

class Tools:
    "Contient des méthodes de calcul et de génération"

    def loi_normale(mu, sigma):
        "Renvoie le premier entier strictement positif généré selon une loi normale."
        n = 0
        while (n<=0):
            n = np.random.randn(1) * sigma + mu
        return int(n[0])

    def gen_nom(sexe,ld):
        "Sexe biologique doit être au format Masculin ou Féminin"
        opener,closer,mid1,mid2,a = random.choice(ld.dict["Opener"]),random.choice(ld.dict["Closer"+sexe[0]]),random.choice(ld.dict["Middle"]),random.choice(ld.dict["Middle"]),random.randrange(3)
        if(a==0): return opener+mid1+mid2+closer
        elif(a==1): return opener+closer+mid1+closer
        else: return opener+closer

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
                            probas.append(int(e.split('%')[0])/100)
                            valeurs.append(e.split('%')[1])
                        # caractère chainé en fonction d'une autre caractéristique + proba
                        # print(f"PROBAS {probas} > VALEURS : {valeurs}")
                        test,cle = key.split('~')[0],key.split('~')[1]
                        filtre,val,comparateur = test.split(' ')[0][2:],test.split(' ')[2],test.split(' ')[1]
                        if(filtre in dico.keys()):
                            if(comparateur=="==" and dico[filtre]==val[1:-1]) or (comparateur=="!=" and dico[filtre]!=val[1:-1]) or (comparateur==">=" and int(dico[filtre])>=int(val)) or (comparateur=="<=" and int(dico[filtre])<=int(val)): dico[cle] = np.random.choice(valeurs,p=probas)
                    else:
                        # on doit sélectionner selon une probabilité simple
                        probas,valeurs = [],[]
                        for e in ld.dict[key]:
                            probas.append(int(e.split('%')[0])/100)
                            valeurs.append(e.split('%')[1])
                        dico[key[1:]] = np.random.choice(valeurs,p=probas)
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

    def pick_car(ld,key,probabiliste):
        "Renvoie une caractéristique aléatoire ou aléatoire pondérée en fonction d'une clé"
        # on doit sélectionner selon une probabilité
        if(probabiliste):
            probas,valeurs = [],[]
            for e in ld.dict[key]:
                probas.append(e.split('%')[0])
                valeurs.append(e.split('%')[1])
            return np.random.choice(valeurs,1,probas)[0]
        # sinon, sélection simple
        return random.choice(ld.dict[key])

    def is_car_ok(filtre,dico,comparateur):
        "Dit si une condition est vérifiée ou non"
        if(filtre in dico.keys()):
            if(comparateur=="=="):
                if(dico[filtre]==val): return True
            if(comparateur==">="):
                if(int(dico[filtre])>=int(val)): return True
            if(comparateur=="<="):
                if(int(dico[filtre])<=int(val)): return True
        return False


    def fill_recursive(ld,sexe,nom,age):
        "Effectue une attribution des caractéristiques annexes"
        blacklist = ["Opener","CloserM","CloserF","Middle"] # paramètres à ne pas rentrer dans le dictionnaire
        dico = {'Nom' : nom,'Age' : age, 'Sexe_biologique' : sexe}
        probabiliste,localKey = False,""
        for key in ld.dict:
            if(key not in blacklist):
                probabiliste = (key[0]=='%')
                localKey = key[1:] # on supprime le symbole % de la clé pour effectuer la suite du traitement
                # on check si on a des paramètres chainés ou non
                if('|' in key):
                    localKey = key.split('~')[0][1:]
                    filtres = key.split('~')[0]

                    

        return dico

    def split_at_logical(l):
        """ renvoie un tuple séparé à la virgule
        
        Keywords arguments:
        l -- string, ligne de lecture
        """
        liste,bl,string = [],False,""
        for c in l:
            if((c!="$") and (c!="&")): string=string+c
            else:
                liste.append(string)
                string = ""
        return liste

        return (str1,str2[:-1]) # on retire le retour charriot

    def splitted_work():
        if(key[0]=='|'):
            # caractère chainé en fonction d'une autre caractéristique
            test,cle = key.split('~')[0],key.split('~')[1]
            filtre,val,comparateur = test.split(' ')[0][1:],test.split(' ')[2],test.split(' ')[1]
            if(filtre in dico.keys()):
                if(comparateur=="!="):
                    if(dico[filtre]!=val): dico[cle] = random.choice(ld.dict[key])
                if(comparateur=="=="):
                    if(dico[filtre]==val): dico[cle] = random.choice(ld.dict[key])
                if(comparateur==">="):
                    if(int(dico[filtre])>=int(val)): dico[cle] = random.choice(ld.dict[key])
                if(comparateur=="<="):
                    if(int(dico[filtre])<=int(val)): dico[cle] = random.choice(ld.dict[key])

class Regexpr:
    "Modélisation d'expression régulières"

    def res(expr):
        "Evaluation d'une expression régulière"
        """
        match expr:
            case Or(expr1,expr2)):
                return (res(expr1) or res(expr2))
            case And(expr1,expr2)):
                return (res(expr1) and res(expr2))
            case Vide() :
                return True

        """
        if (expr == Or(expr1,expr2)):
            return (res(expr1) or res(expr2))
        if (expr == And(expr1,expr2)):
            return (res(expr1) and res(expr2))
        else: return True

    class Or:
        def __init__(self,expr1,expr2):
            self.a = expr1
            self.b = expr2

    class And:
        def __init__(self,expr1,expr2):
            self.a = expr1
            self.b = expr2

    class Vide:
        def __init__(self):
            pass
      


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
