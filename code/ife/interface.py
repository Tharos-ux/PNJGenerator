from tkinter import *
from functools import partial
from tkinter.filedialog import asksaveasfile
import platform
import reg.pnj as p

def linearisationSave(monPnj):
    "Renvoie les éléments d'un PnJ sous forme de texte afin de l'enregistrer"
    string=""
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
        listePnj[index] = p.Pnj(ld,pnj,charac)
        # on récupère la caractéristique d'intérêt
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
        "définit un conteneur d'info avec son bouton refresh"

        def __init__(self,entree,contenu,fenetre):
                "Initialise un nouveau conteneur"
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
        if (k not in ["Opener","CloserM","CloserF","Middle"]) and (v != None):
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
        "Fonction qui met à jour les textes & boutons au changement de PnJ"
        global index
        global listePnj
        listePnj[index].desc = notes.get("1.0",END)
        index+=indent
        if(index>=len(listePnj)):
            listePnj.append(p.Pnj(ld))
            index = len(listePnj)-1    
        elif(index<0):
            index = 0
        builder(fenetre,listePnj[index].carac,pan,master)

    def filesave(a):
        "Commande du bouton sauvegarder"
        global index
        listePnj[index].desc = notes.get("1.0",END)
        files = [('Document texte', '*.txt')]
        fichier = asksaveasfile(filetypes = files, defaultextension = files)
        fichier.write(linearisationSave(listePnj[index]))
        fichier.close()

def affichage(listedico):

    # Constantes et globales
    COLOR="#36393f"
    global ld
    global listePnj
    global index
    global imgbutton
    ld = listedico
    listePnj = [p.Pnj(ld)] # le Pnj créé initialement est mis dans la liste
    index = 0

    # Déclaration de la fenêtre
    fenetre = Tk()
    
    # Déplacements de la barre de dialogue
    def move_window(event):
        fenetre.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

    fenetre.geometry("450x900+75+75")
    fenetre['background']="#2f3136"
    # make a frame for the title bar
    imgbutton = PhotoImage(file='ife/button.png')
    img = PhotoImage(file='ife/title.png')

    # barre de titre
    title_bar = Frame(fenetre, bg='#2f3136', relief='flat', bd=0)
    title_text = Label(title_bar,fg="#FFFFFF",bg="#2f3136", text="PNJMaker", image=img, font=('Aerial', 12, 'bold'))

    match platform.system():
        case 'Linux':
            fenetre.attributes('-type', 'dock')
        case 'Windows' | 'Darwin' :
            fenetre.overrideredirect(True)
            title_bar.bind('<B1-Motion>', move_window)
        case _:
            # fenetre.wm_attributes('-fullscreen', 'True')
            pass # on ne sait pas quel système c'est, on utilise l'affichage par défaut

    window = Canvas(fenetre, bg=COLOR, bd=0, width=450, height=550, highlightthickness=0, relief='ridge')

    title_bar.pack(expand=1, fill=X)
    title_text.pack(side=TOP)

    window.pack(fill='both')

    # Construction du layout
    pan = None # baba is nothing
    builder(window,listePnj[index].carac,pan,fenetre)

    """
    #barre d'état
    status_bar = Frame(fenetre, bg='#2f3136', relief='flat', bd=0)
    status_text = Label(status_bar,fg="#FFFFFF",bg="#2f3136", text="Texte d'état", font=('Aerial', 12, 'bold'))
    status_bar.pack(expand=1, fill='none')
    status_text.pack(side=BOTTOM)
    """

    # permet de renvoyer la fenêtre à l'arrière en cas de perte de focus
    fenetre.lift()
    fenetre.attributes('-topmost',True)
    fenetre.after_idle(fenetre.attributes,'-topmost',False)

    # Boucle d'exécution
    fenetre.mainloop()
