#!/usr/bin/python3.10

import random
import sys
import interfaceAlt
import numpy

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
        interfaceAlt.affichage(ld)
        
def nouveauPnj(ld,pnj=None,charac=None):
    return Pnj(ld,current=pnj,change=charac)


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

class Tools:
    "Contient des méthodes de calcul et de génération"

    def loi_normale(mu, sigma):
        "Renvoie le premier entier strictement positif généré selon une loi normale."
        n = 0
        while (n<=0):
            n = numpy.random.normal(sigma,mu,1)[0]
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

    def gen_nom(sexe,ld,composed=True,neuralInput=False):
        "Sexe biologique doit être au format Masculin ou Féminin"
        opener,closer,mid1,mid2,a = random.choice(ld.dict["Opener"]),random.choice(ld.dict["Closer"+sexe[0]]),random.choice(ld.dict["Middle"]),random.choice(ld.dict["Middle"]),random.randrange(3)
        if(neuralInput): # renvoie une liste
            if(a==0): return (NeuralPrep.convert_to_ints(opener+mid1+mid2+closer),opener+mid1+mid2+closer)
            elif(a==1): return (NeuralPrep.convert_to_ints(opener+mid1+closer),opener+mid1+closer)
            else: return (NeuralPrep.convert_to_ints(opener+closer),opener+closer)
        elif(composed): # renvoie un nom
            if(a==0): return opener+mid1+mid2+closer
            elif(a==1): return opener+mid1+closer
            else: return opener+closer
        else:
            if(a==0): return f"{opener},{mid1},{mid2},{closer},{opener}{mid1}{mid2}{closer},{sexe[0]}"
            elif(a==1): return f"{opener},{mid1},,{closer},{opener}{mid1}{closer},{sexe[0]}"
            else: return f"{opener},,,{closer},{opener}{closer},{sexe[0]}"

    def fill_regexpr(ld,dico,blacklist=["Opener","CloserM","CloserF","Middle"]):
        "Effectue une attribution des caractéristiques annexes"
        constraints = dict()
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
                        if(Regexpr.res(conversion(test),dico)):
                            dico[cle] = Tools.weighted_choice(valeurs,probas)
                            constraints[cle] = test
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
                    if(Regexpr.res(conversion(test),dico)):
                        dico[cle] = random.choice(ld.dict[key])
                        constraints[cle] = test
                else:
                    # sélection aléatoire basique
                    dico[key] = random.choice(ld.dict[key])
        return (dico,constraints)

class Pnj:
    "Contient les méthodes permettant de créer un objet PnJ"

    def __init__(self,ld,current=None,change=None):
        "Initialise un nouvel objet PnJ"
        match current:
            case None:
                self.sexe = "Féminin" if(random.randrange(2)==0) else "Masculin"
                self.name = Tools.gen_nom(self.sexe,ld)
                self.age = Tools.loi_normale(30,8)
                self.carac,self.constraints = Tools.fill_regexpr(ld,{'Nom' : self.name,'Age' : self.age, 'Sexe_biologique' : self.sexe})
                self.desc = ""
            case _:
                self.sexe = current.sexe
                self.name = current.name
                self.age = current.age
                match change:
                    case 'Sexe_biologique':
                        # on intervertit l'état
                        self.sexe = current.carac['Sexe_biologique'] = "Féminin" if(current.carac['Sexe_biologique']=="Masculin") else "Masculin"
                    case 'Nom':
                        # on reroll un nom
                        self.name = current.carac['Nom'] = Tools.gen_nom(self.sexe,ld,composed=True)
                    case 'Age':
                        self.age = current.carac['Age'] = Tools.loi_normale(30,8)
                    case car:
                        # TODO chaining des expressions par arbres
                        list_reroll = []
                        for char,filtre in current.constraints.items():
                            if (car in filtre): list_reroll.append(char)
                        blacklist = [key for key in current.carac if key != car]
                        nextchar = current.carac[car]
                        while nextchar==current.carac[car]:
                            newchars = Tools.fill_regexpr(ld,current.carac.copy(),blacklist)[0]
                            nextchar = newchars[car]
                        current.carac[car] = newchars[car]

                        # may work but need test
                        blacklist = [key for key in current.carac if key not in list_reroll]
                        newchars,self.constraints = Tools.fill_regexpr(ld,{'Nom' : self.name,'Age' : self.age, 'Sexe_biologique' : self.sexe, change : current.carac[change]},blacklist)
                        charlist = Tools.fill_regexpr(ld,{'Nom' : self.name,'Age' : self.age, 'Sexe_biologique' : self.sexe, change : current.carac[change]},["Opener","CloserM","CloserF","Middle"])[0].keys()
                        print(charlist)
                        for e in list_reroll:
                            current.carac[e] = newchars[e]

                        newdict = dict()
                        for key in charlist:
                            newdict[key] = newchars[key] if key in newchars.keys() else current.carac[key]
                        current.carac = newdict
                        
                self.carac = current.carac
                self.desc = current.desc

    def __str__(self):
        "Renvoie une description du PnJ"
        return f"{self.name} est âgé de {self.age} ans."

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

class Regexpr:
    "Classe permettant la modélisation d'expression régulières"

    def res(expr,dico):
        """Fonction permettant l'évaluation d'une expression régulière

        Keywords arguments:
        expr - un objet de type Regexpr
        dico - un dictionnaire, données d'exécution du programme
        """
        match expr:
            case Regexpr.Or(expr1,expr2):
                return (Regexpr.res(expr1,dico) or Regexpr.res(expr2,dico))
            case Regexpr.And(expr1,expr2):
                return (Regexpr.res(expr1,dico) and Regexpr.res(expr2,dico))
            case Regexpr.Vide():
                return True
            case Regexpr.Element(cle,comparateur,valeur):
                return Regexpr.evaluate(cle,comparateur,valeur,dico)
            case True | False:
                return expr
            case _:
                return False

    def evaluate(filtre,comparateur,val,dico):
        """Evalue le résultat d'une condition locale, et renvoie sa validité
        
        Keywords arguments:
        filtre - str, clé pouvant ou non être présente dans la dico
        comparateur - str, opérateur
        val - str, valeur associée au filtre à chercher dans le dico
        dico - un dictionnaire, données d'exécution du programme
        """
        if(filtre in dico.keys()):
            if(comparateur=="==" and dico[filtre]==val[1:-1]) or (comparateur=="!=" and dico[filtre]!=val[1:-1]) or (comparateur==">=" and int(dico[filtre])>=int(val)) or (comparateur=="<=" and int(dico[filtre])<=int(val)):
                return True
        return False

    class Or:
        "Opérateur logique OU"
        __match_args__ = ("a", "b") 
        def __init__(self,expr1,expr2):
            self.a = expr1
            self.b = expr2
        
        def __str__(self):
            return f"Or({self.a},{self.b})"

    class And:
        "Opérateur logique ET"
        __match_args__ = ("a", "b") 
        def __init__(self,expr1,expr2):
            self.a = expr1
            self.b = expr2

        def __str__(self):
            return f"And({self.a},{self.b})"

    class Element:
        "Element, plus bas niveau d'existence"
        __match_args__ = ("a","comp","b") 
        def __init__(self,cle,comparateur,valeur):
            self.a = cle
            self.comp = comparateur
            self.b = valeur

        def __str__(self):
            return f"{self.a} {self.comp} {self.b}"

    class Vide:
        "Modélise le vide"
        def __init__(self):
            pass
        
        def __str__(self):
            return "NA"


# si on lance via ligne de commande, on exécute la fonction main
if __name__ == "__main__":
    main()
