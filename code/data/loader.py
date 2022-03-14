def open_dico(fichier:str) -> dict:
    """Chargement du fichier de données en un dico de listes
    le symbole dièse sera la marque d'un commentaire dans le fichier
    Keywords arguments
    fichier - str, adresse d'un fichier à lire
     """
    with open(fichier,"r", encoding="utf-8") as reader:
        return {l[:-1].split(":")[0]:(l[:-1].split(":")[1]).split(",") for l in reader if(l[0]!='#')}

"""
        for l in reader:
            if(l[0]!='#'):
                l = l[:-1]
                a,b = l.split(":")[0],l.split(":")[1]
                dico[a] = b.split(",")
    return dico
"""