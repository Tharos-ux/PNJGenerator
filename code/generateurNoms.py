import main

def sauvegarde(texteA,texteB):
    with open("noms.css","w") as writer:
        for e in texteA:
            writer.write(f"{e}\n")
        for e in texteB:
            writer.write(f"{e}\n")

def core():
    listM,listF = [],[]
    ld = main.Loader("data.ini")
    for _ in range(1000):
        listM.append(main.Tools.gen_nom("Masculin",ld,composed=False))
        listF.append(main.Tools.gen_nom("Féminin",ld,composed=False))
    sauvegarde(listM,listF)

core()
    