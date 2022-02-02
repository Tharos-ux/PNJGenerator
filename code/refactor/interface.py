from tkinter import *

fenetre = Tk()
fenetre.title("Refactor")
fenetre.geometry("500x300")


dico = {"texte 1":"entree 1", "texte 2":"entree 2", "texte 3":"entree 3", "texte 4":"entree 4", "texte 5":"entree 5", "texte 6":"entree 6"}


class Conteneur:
    # définit un conteneur d'info avec son bouton refresh
    def __init__(self,entree,contenu,fenetre):
            "Initialise un nouvel objet PnJ"
            self.entreeDico = entree
            self.texte = contenu
            # méthodes graphiques
            self.panl = PanedWindow(orient = 'horizontal')
            self.panl.pack(fill=BOTH,expand=1)
            self.labl = Label(self.panl, text=self.entreeDico, font=('Aerial', 10))
            self.panl.add(self.labl)
            self.varl = Label(self.panl, text=self.texte, font=('Aerial', 10))
            self.panl.add(self.varl)
            self.button = Button(self.panl, text="Refresh",bg='black', fg='white', command=fenetre.destroy)
            self.panl.add(self.button)

def builder(fenetre,dico):
    """ Sert à construire l'interface interne de la fenêtre.
    
    Keywords arguments
    fenetre -- le conteneur parent
    dico -- le contenu à afficher
    """
    for k,v in dico.items():
        pawin = Conteneur(k,v,fenetre).panl
        pawin.pack(fill = BOTH, expand = True)

fenetre.mainloop()