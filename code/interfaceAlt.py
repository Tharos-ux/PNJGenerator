from tkinter import *
from tkinter import ttk
import main

def linearisation(monPnj):
    string=""
    for key in monPnj.carac:
        string = string + f"{key.replace('_',' ')} = {monPnj.carac[key]}\n"
    return string

def linearisationSave(monPnj):
    string="---------------------\n"
    for key in monPnj.carac:
        string = string + f"{key.replace('_',' ')} = {monPnj.carac[key]}\n"
    return string

class Windowbject:
    # définit une entité fenêtre
    def __init__(self):
        self.fen = Tk()
        self.fen.geometry("500x850")
        self.fen.title("PNJMaker")
        self.pane = builder


class Conteneur:
    # définit un conteneur d'info avec son bouton refresh
    def __init__(self,entree,contenu,fenetre):
            "Initialise un nouvel objet PnJ"
            self.entreeDico = entree
            self.texte = contenu
            # méthodes graphiques
            #self.panl = PanedWindow(orient = 'horizontal')
            #self.panl.pack(fill=BOTH,expand=1)
            self.labl = Label(fenetre, text=str(self.entreeDico).replace('_',' '), font=('Aerial', 10))
            #self.panl.add(self.labl)
            self.varl = Label(fenetre, text=str(self.texte).replace('_',' '), font=('Aerial', 10))
            #self.panl.add(self.varl)
            self.button = Button(fenetre, text="Refresh",bg='black', fg='white', command=fenetre.destroy, state=DISABLED)
            #self.panl.add(self.button)

def builder(fenetre,dico,pan):
    """ Sert à construire l'interface interne de la fenêtre.
    
    Keywords arguments
    fenetre -- le conteneur parent
    dico -- le contenu à afficher
    """
    global index

    # on nettoie tout
    for widgets in fenetre.winfo_children():
        widgets.destroy()
    
    #TODO
    root.columnconfigure(0, weight=1)
    # on reforme l'interface
    count = 0
    for k,v in dico.items():
        pan = Conteneur(k,v,fenetre)
        pan.labl.grid(row=count,column=0)
        pan.varl.grid(row=count,column=1,columnspan=2)
        pan.button.grid(row=count,column=3)
        #pan.pack(padx=5, pady=5,side=TOP) #(fill = BOTH, expand = True)
        count+=1

    #cadre = Frame(fenetre)
    #cadre.pack(padx=5, pady=5,side=BOTTOM)
    # changer de pnj
    btnGauche = Button(fenetre, text='<', bg='black', fg='white', command=lambda indent=-1 : actualise(indent))
    #btnGauche.pack(padx=5, pady=5, side=LEFT)
    btnGauche.grid(row=count+1,column=0)
    #btnGauche["state"] = "disabled"
    
    # quitter
    btnQuit = Button(fenetre, text='Quitter',bg='black', fg='white', command=fenetre.destroy)
    btnQuit.grid(row=count+1,column=1)
    #.pack(padx=5, pady=5, side=LEFT, expand=1)
    btnSave = Button(fenetre, text='Sauver', bg='black', fg='white', command=lambda indent=0 : sauvegarde(indent))
    btnSave.grid(row=count+1,column=2)
    #btnSave.pack(padx=5, pady=5, side=LEFT)
    btnDroite = Button(fenetre, text='>', bg='black', fg='white', command=lambda indent=1 : actualise(indent))
    #btnDroite.pack(padx=5, pady=5, side=LEFT)
    btnDroite.grid(row=count+1,column=3)

    if(index<=0):
        btnGauche["state"] = "disabled"
    else:
        btnGauche["state"] = "normal"

    def actualise(indent):
        "Fonction qui met à jour les textes & boutons"
        global index
        global listePnj
        index+=indent
        if(index>=len(listePnj)):
            listePnj.append(main.nouveauPnj(ld))
            index = len(listePnj)-1    
        elif(index<0):
            index = 0
        builder(fenetre,listePnj[index].carac,pan)

    def sauvegarde(a):
        global index
        with open("sauvegardes.txt","a") as writer:
            writer.write(linearisationSave(listePnj[index]))
    
    def reroll(charac,pnj,ld):
        # on crée un nouveau template de PnJ de base, temporaire
        container = main.nouveauPnj(ld)
        # on récupère la caractéristique d'intérêt
        pnj.carac
        # on actualise l'affichage
        label["text"] = linearisation(pnj)

def affichage(listedico):
    global ld
    ld = listedico
    global listePnj
    listePnj = [main.nouveauPnj(ld)] # le Pnj créé initialement est mis dans la liste
    global index
    index = 0
    fenetre = Tk()
    fenetre.geometry("500x850")
    fenetre.title("PNJMaker")
    pan = None # baba is nothing
    builder(fenetre,listePnj[index].carac,pan)

    # boucle d'exécution
    fenetre.mainloop()

"""
def actualise(indent):
    "Fonction qui met à jour les textes & boutons"
    global index
    global listePnj
    index+=indent
    if(index>=len(listePnj)):
        listePnj.append(main.nouveauPnj(ld))
        index = len(listePnj)-1
    elif(index<0):
        index = 0
    if(index==0): btnGauche["state"] = "disabled"
    else: btnGauche["state"] = "normal"
    builder(fenetre,listePnj[index].carac,pan)
        #label["text"] = linearisation(listePnj[index])
"""
    