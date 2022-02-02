
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

