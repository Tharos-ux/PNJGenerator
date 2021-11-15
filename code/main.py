import numpy as np

def main():
    monPnj = Pnj("Ulfric Sombrage")
    print(monPnj)

class Tools:
    def loi_normale(mu, sigma):
        n = np.random.randn(1) * sigma + mu
        return int(n[0])

class Pnj:
    def __init__(self,name):
        self.name = name
        self.age = Tools.loi_normale(25,15)

    def __str__(self):
        return f"{self.name} est âgé de {self.age} ans."


# si on lance via ligne de commande, on exécute la fonction main
if __name__ == "__main__":
    main()
