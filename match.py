#!/usr/bin/python3.10

class Regexpr:
    "Modélisation d'expression régulières"

    def res(expr):
        "Evaluation d'une expression régulière"
        match expr:
            case Regexpr.Or(expr1,expr2):
                print("On détecte un OR")
                return (Regexpr.res(expr1) or Regexpr.res(expr2))
            case Regexpr.And(expr1,expr2):
                print("On détecte un AND")
                return (Regexpr.res(expr1) and Regexpr.res(expr2))
            case Regexpr.Vide():
                return True
            case Regexpr.Element(cle,comparateur,valeur):
                return Regexpr.evaluate(cle,comparateur,valeur)
            case True:
                return True
            case False:
                return False

    def evaluate(filtre,comparateur,val):
        dico = {"Texte": "Texte"}
        if(filtre in dico.keys()):
            print("indico")
            if(comparateur=="==" and dico[filtre]==val) or (comparateur=="!=" and dico[filtre]!=val) or (comparateur==">=" and int(dico[filtre])>=int(val)) or (comparateur=="<=" and int(dico[filtre])<=int(val)):
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

    

#expression = Regexpr.And(True,True)

#print(Regexpr.res(Regexpr.Element("Texte","==","Texte")))

#Ethnie == "Alastraar" & Age >= 20~Test:valide
def conversion(string):
    # quand on arrive ici, on considère que la chaine est chainée
    #ischained = ('|' in string)
    #isproba = ('%' in string)
    string = string.replace('|').replace('%') # on supprime les tags
    islogical = ('&' in string) or ('$' in string)
    hasparenthesis = ('(' in string) or (')' in string)
    match [islogical,hasparenthesis]:
        case [False,_]:
            return Regexpr.Vide()
        case [True,False]:
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

#print('Test == aaaa & Oui === bbbb'.split(' ')[4:])

print(conv('Test == aaaa & Oui == bbbb $ Non == cccc'.split(' ')))

"""
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
"""                    


"""
    def split_at_logical(l):
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



print(Regexpr.res(expression))

"""