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

def conversion(nom):
    nom = nom.lower()
    liste = []
    for l in nom:
        liste.append(cv(l))
    return liste
