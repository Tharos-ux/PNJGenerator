import random
import numpy as np

def main():
    ld = Loader("/home/siegfried/Python/PNJMaker/ressources/data.ini")
    monPnj = Pnj(ld)
    print(monPnj)

class Tools:
    def loi_normale(mu, sigma):
        "Renvoie le premier entier strictement positif généré selon une loi normale."
        n = 0
        while (n<=0):
            n = np.random.randn(1) * sigma + mu
        return int(n[0])

    def gen_nom(sexe,ld):
        "Sexe doit être au format M ou F"
        opener,closer,mid1,mid2,a = random.choice(ld.dict["Opener"]),random.choice(ld.dict["Closer"+sexe]),random.choice(ld.dict["Middle"]),random.choice(ld.dict["Middle"]),random.randrange(3)
        if(a==0): return opener+mid1+mid2+closer
        elif(a==1): return opener+closer+mid1+closer
        else: return opener+closer

class Pnj:
    def __init__(self,ld):
        "Initialise un nouvel objet PnJ"
        self.sexe = "F" if(random.randrange(1)==0) else "M"
        self.name = Tools.gen_nom(self.sexe,ld)
        self.age = Tools.loi_normale(30,20)

    def __str__(self):
        "Renvoie une description du PnJ"
        return f"{self.name} est âgé de {self.age} ans."

class Loader:
    def __init__(self,fichier):
        "Chargement du fichier de données en un dico de listes"
        self.dict = {}
        with open(fichier,"r") as reader:
            for l in reader:
                l = l[:-1]
                a,b = l.split(":")[0],l.split(":")[1]
                self.dict[a] = b.split(",")



# si on lance via ligne de commande, on exécute la fonction main
if __name__ == "__main__":
    main()
