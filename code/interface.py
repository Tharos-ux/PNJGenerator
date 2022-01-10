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

def affichage(ld):
    listePnj = [main.nouveauPnj(ld)] # le Pnj créé initialement est mis dans la liste
    global index
    index = 0
    fenetre = Tk()
    fenetre.geometry("300x350")
    fenetre.title("PNJMaker")
    label= Label(fenetre, text= linearisation(listePnj[index]), font= ('Aerial', 10))
    label.pack()
    cadre = Frame(fenetre)
    cadre.pack(padx=5, pady=5,side=BOTTOM)
    # changer de pnj
    btnGauche = Button(cadre, text='<', bg='black', fg='white', command=lambda indent=-1 : actualise(indent))
    btnGauche.pack(padx=5, pady=5, side=LEFT)
    btnGauche["state"] = "disabled"
    # quitter
    Button(cadre, text='Quitter',bg='black', fg='white', command=fenetre.destroy).pack(padx=5, pady=5, side=LEFT, expand=1)
    btnSave = Button(cadre, text='Sauver', bg='black', fg='white', command=lambda indent=0 : sauvegarde(indent))
    btnSave.pack(padx=5, pady=5, side=LEFT)
    btnDroite = Button(cadre, text='>', bg='black', fg='white', command=lambda indent=1 : actualise(indent))
    btnDroite.pack(padx=5, pady=5, side=LEFT)

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

    def actualise(indent):
        "Fonction qui met à jour les textes & boutons"
        global index
        index+=indent
        if(index>=len(listePnj)):
            listePnj.append(main.nouveauPnj(ld))
            index = len(listePnj)-1
        elif(index<0):
            index = 0
        if(index==0): btnGauche["state"] = "disabled"
        else: btnGauche["state"] = "normal"
        label["text"] = linearisation(listePnj[index])

    class Containt:
        "Contient les méthodes permettant de créer un objet d'interface"

        def __init__(self,entree,contenu):
            "Initialise un nouvel objet PnJ"
            self.entreeDico = entree
            self.texte = contenu
            # méthodes graphiques
            self.label = Label(fenetre, contenu, font= ('Aerial', 10))
            self.button = Button(cadre, text='Reload',bg='black', fg='white', command=fenetre.destroy)

    fenetre.mainloop()