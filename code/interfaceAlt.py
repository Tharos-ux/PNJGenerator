from tkinter import *
import main
from functools import partial
from tkinter.filedialog import asksaveasfile

def linearisation(monPnj):
    string=""
    for key in monPnj.carac:
        string = string + f"{key.replace('_',' ')} = {monPnj.carac[key]}\n"
    return f"{string}\n{monPnj.desc}"

def linearisationSave(monPnj):
    string="---------------------\n"
    for key in monPnj.carac:
        string = string + f"{key.replace('_',' ')} = {monPnj.carac[key]}\n"
    return f"{string}\n{monPnj.desc}"




def builder(fenetre,dico,pan,master):
    """ Sert à construire l'interface interne de la fenêtre.
    
    Keywords arguments
    fenetre -- le conteneur parent
    dico -- le contenu à afficher
    """
    # Constantes et globales
    PAD = 1
    WGRID = 150
    COLOR="#36393f"
    global index
    global listePnj
    
    # Layout
    fenetre.columnconfigure(0, weight=1, minsize=WGRID)
    fenetre.columnconfigure(1, weight=1, minsize=WGRID/2)
    fenetre.columnconfigure(2, weight=1, minsize=WGRID/2)
    fenetre.columnconfigure(3, weight=1, minsize=WGRID)

    # Nettoyage de l'interface
    for widgets in fenetre.winfo_children():
        widgets.destroy()

    def reroll(charac,pnj,ld,fenetre,dico,pan,master):
        listePnj[index].desc = notes.get("1.0",END)
        # on crée un nouveau template de PnJ de base, temporaire
        new_pnj = main.nouveauPnj(ld)
        # on récupère la caractéristique d'intérêt
        pnj.carac[charac] = new_pnj.carac[charac]
        # on actualise l'affichage
        builder(fenetre,dico,pan,master)

    # Boutons de menu
    btnGauche = Button(fenetre, bd=0, relief=FLAT, text='<', bg='#2f3136', fg='white', command=lambda indent=-1 : actualise(indent))
    btnGauche.grid(row=0,column=0, padx=PAD, pady=PAD*10)
    btnQuit = Button(fenetre, bd=0, relief=FLAT, text='Quitter',bg='#2f3136', fg='white', command=master.destroy)
    btnQuit.grid(row=0,column=1, padx=PAD, pady=PAD*10)
    btnSave = Button(fenetre, bd=0, relief=FLAT, text='Sauver', bg='#2f3136', fg='white', command=lambda indent=0 : filesave(indent))
    btnSave.grid(row=0,column=2, padx=PAD, pady=PAD*10)
    btnDroite = Button(fenetre, bd=0, relief=FLAT, text='>', bg='#2f3136', fg='white', command=lambda indent=1 : actualise(indent))
    btnDroite.grid(row=0,column=3, padx=PAD, pady=PAD*10)
    
    
    class Conteneur:
    # définit un conteneur d'info avec son bouton refresh
        def __init__(self,entree,contenu,fenetre):
                "Initialise un nouvel objet PnJ"
                global imgbutton
                self.entreeDico = entree
                self.texte = contenu
                self.labl = Label(fenetre,fg="#FFFFFF",bg="#36393f", text=str(self.entreeDico).replace('_',' '), font=('Aerial', 10))
                self.varl = Label(fenetre,fg="#FFFFFF",bg="#36393f", text=str(self.texte).replace('_',' '), font=('Aerial', 12, 'bold'))
                self.action = partial(reroll, self.entreeDico, listePnj[index], ld, fenetre, dico, pan, master)
                self.button = Button(fenetre, bd=0, relief=FLAT, text="Refresh",bg='#36393f', fg='white', image = imgbutton, command=self.action)

    count = 1
    # Zone de description
    for k,v in dico.items():
        pan = Conteneur(k,v,fenetre)
        pan.labl.grid(row=count,column=0, padx=PAD, pady=PAD)
        pan.varl.grid(row=count,column=1,columnspan=2, padx=PAD, pady=PAD)
        pan.button.grid(row=count,column=3, padx=PAD, pady=PAD)
        count+=1

    # Etat des boutons du menu
    if(index<=0):
        btnGauche["state"] = "disabled"
    else:
        btnGauche["state"] = "normal"
    
    # Zone de notes
    notes = Text(fenetre, bg = "#40444b", fg = "white", relief='flat', font=('Aerial', 10))
    notes.delete("1.0","end")
    notes.insert("1.0", listePnj[index].desc)
    notes.grid(row=count+1, columnspan=4, padx=PAD*10, pady=PAD*10)

    def actualise(indent):
        "Fonction qui met à jour les textes & boutons"
        global index
        global listePnj
        listePnj[index].desc = notes.get("1.0",END)
        index+=indent
        if(index>=len(listePnj)):
            listePnj.append(main.nouveauPnj(ld))
            index = len(listePnj)-1    
        elif(index<0):
            index = 0
        builder(fenetre,listePnj[index].carac,pan,master)

    def sauvegarde(a):
        global index
        listePnj[index].desc = notes.get("1.0",END)
        with open("sauvegardes.txt","a") as writer:
            writer.write(linearisationSave(listePnj[index]))

    def filesave(a):
        global index
        listePnj[index].desc = notes.get("1.0",END)
        files = [('All Files', '*.*'), 
             ('Document texte', '*.txt')]
        fichier = asksaveasfile(filetypes = files, defaultextension = files)
        fichier.write(linearisationSave(listePnj[index]))
        fichier.close()
        # TODO : ramener la fenêtre à l'arrière plan


def affichage(listedico):

    # Constantes et globales
    COLOR="#36393f"
    global ld
    global listePnj
    global index
    global imgbutton
    ld = listedico
    listePnj = [main.nouveauPnj(ld)] # le Pnj créé initialement est mis dans la liste
    index = 0

    # Déclaration de la fenêtre
    fenetre = Tk()
    
    # Nouvelle barre de dialogue
    def move_window(event):
        fenetre.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

    fenetre.overrideredirect(True) # turns off title bar, geometry
    fenetre.geometry("450x600+200+200")
    fenetre['background']="#2f3136"
    # make a frame for the title bar
    imgbutton = PhotoImage(file='button.png')
    img = PhotoImage(file='title.png')
    title_bar = Frame(fenetre, bg='#2f3136', relief='flat', bd=0)
    title_text = Label(title_bar,fg="#FFFFFF",bg="#2f3136", text="PNJMaker", image=img, font=('Aerial', 12, 'bold'))

    # put a close button on the title bar
    # close_button = Button(title_bar, text='X', command=fenetre.destroy)

    # a canvas for the main area of the window
    window = Canvas(fenetre, bg=COLOR, bd=0, width=450, height=550, highlightthickness=0, relief='ridge')

    # pack the widgets
    title_bar.pack(expand=1, fill=X)
    title_text.pack(side=TOP)
    window.pack(fill='both')

    # bind title bar motion to the move window function
    title_bar.bind('<B1-Motion>', move_window)

    # Construction du layout
    pan = None # baba is nothing
    builder(window,listePnj[index].carac,pan,fenetre)

    # Boucle d'exécution
    fenetre.mainloop()
