import enum
import reg.tools as t
import random
from reg.my_checker import my_class_checker
from enum import Enum,auto
from typing import overload

class Sexe(Enum):
    "Modélise le sexe su PnJ"
    M = "Masculin"
    F = "Féminin"

@my_class_checker
class Pnj:
    "Contient les méthodes permettant de créer un objet PnJ"

    def __init__(self,ld:dict):
        "Initialise un nouvel objet PnJ"
        self.dico = ld
        self.sexe = Sexe.F if(random.randrange(2)==0) else Sexe.M
        self.name = self.gen_name()
        self.age = t.Tools.loi_normale(30,8)
        self.carac,self.constraints = t.Tools.fill_regexpr(self.dico,{'Nom' : self.name,'Age' : self.age, 'Sexe_biologique' : self.sexe})
        self.desc = ""

    def roll_carac(self,caract:str):
        "Effectue le reroll d'une caractéristique"
        match caract:
            case 'Sexe_biologique':
                self.sexe,temp = Sexe.F if self.sexe == Sexe.M else Sexe.M
            case 'Nom':
                self.name,temp = self.gen_name()
            case 'Age':
                self.age,temp = t.Tools.loi_normale(30,8)
            case _:
                temp = None
        self.carac[caract] = temp
            
    @property
    def sexe(self) -> str:
        return self.__sexe.value

    @sexe.setter
    def sexe(self,sexe_bio:Sexe) -> None:
        self.__sexe = sexe_bio

    @property
    def desc(self) -> str:
        return self.__desc

    @desc.setter
    def desc(self,new_desc:str) -> None:
        self.__desc = new_desc

    @property
    def dico(self) -> dict:
        return self.__dico

    @dico.setter
    def dico(self,new_dict:dict) -> None:
        self.__dico = new_dict  

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self,new_name:str) -> None:
        self.__name = new_name

    def gen_name(self) -> str:
        "Sexe biologique doit être au format Masculin ou Féminin"
        opener,closer,mid1,mid2,a = random.choice(self.dico["Opener"]), random.choice(self.dico[f"Closer{self.sexe[0]}"]), random.choice(self.dico["Middle"]), random.choice(self.dico["Middle"]), random.randrange(3)
        match a:
            case 0:
                return f"{opener}{mid1}{mid2}{closer}"
            case 1:
                return f"{opener}{mid1}{closer}"
            case _:
                return f"{opener}{closer}"
    
    def __str__(self):
        "Renvoie une description du PnJ"
        return f"{self.name} est âgé de {self.age} ans."

"""
    def reroll(self,carac:str):
        "Reroll une caractéristique d'un PnJ basée sur son dictionnaire"

                match change:
                    case car:
                        # TODO chaining des expressions par arbres
                        list_reroll = []
                        for char,filtre in current.constraints.items():
                            if (car in filtre): list_reroll.append(char)
                        blacklist = [key for key in current.carac if key != car]
                        nextchar = current.carac[car]
                        while nextchar==current.carac[car]:
                            newchars = t.Tools.fill_regexpr(self.dico,current.carac.copy(),blacklist)[0]
                            nextchar = newchars[car]
                        current.carac[car] = newchars[car]

                        # may work but need test
                        blacklist = [key for key in current.carac if key not in list_reroll]
                        newchars,self.constraints = t.Tools.fill_regexpr(self.dico,{'Nom' : self.name,'Age' : self.age, 'Sexe_biologique' : self.sexe, change : current.carac[change]},blacklist)
                        charlist = t.Tools.fill_regexpr(self.dico,{'Nom' : self.name,'Age' : self.age, 'Sexe_biologique' : self.sexe, change : current.carac[change]},["Opener","CloserM","CloserF","Middle"])[0].keys()
                        print(charlist)
                        for e in list_reroll:
                            current.carac[e] = newchars[e]

                        newdict = dict()
                        for key in charlist:
                            newdict[key] = newchars[key] if key in newchars.keys() else current.carac[key]
                        current.carac = newdict
                        
                self.carac = current.carac
                self.desc = current.desc
"""