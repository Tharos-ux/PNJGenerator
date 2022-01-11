import main

def sauvegarde(texteA,texteB):
    with open("noms.csv","w") as writer:
        for e in texteA:
            writer.write(f"{e},M\n")
        for e in texteB:
            writer.write(f"{e},F\n")

def core():
    listM,listF = [],[]
    ld = main.Loader("data.ini")
    for _ in range(1000):
        nomM,nomF = main.Tools.gen_nom("Masculin",ld,neuralInput=True),main.Tools.gen_nom("Féminin",ld,neuralInput=True) # tuples
        listMt=[str(x) for x in nomM[0]]
        listFt=[str(x) for x in nomF[0]]
        listMt,listFt = ','.join(listMt),','.join(listFt)
        listF.append(f"{listFt},{nomF[1]}")
        listM.append(f"{listMt},{nomM[1]}")
    sauvegarde(listM,listF)

core()
    