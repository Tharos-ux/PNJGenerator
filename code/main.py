import random
import numpy as np

def main():
    ld = Loader("/home/siegfried/Python/PNJMaker/ressources/data.ini")
    monPnj = Pnj(ld)
    print(monPnj)

class Tools:
    def loi_normale(mu, sigma):
        n = np.random.randn(1) * sigma + mu
        return int(n[0])

class Pnj:
    def __init__(self,ld):
        self.name = random.choice(ld.dict["Nom"])
        self.age = Tools.loi_normale(25,15)

    def __str__(self):
        return f"{self.name} est âgé de {self.age} ans."

class Loader:
    def __init__(self,fichier):
        "Dico de listes"
        self.dict = {}
        with open(fichier,"r") as reader:
            for l in reader:
                l = l[:-1]
                a,b = l.split(":")[0],l.split(":")[1]
                self.dict[a] = b.split(",")



# si on lance via ligne de commande, on exécute la fonction main
if __name__ == "__main__":
    main()
