#!/usr/bin/python3.10

import sys
import ife.interface as f
import reg.regexpr as r
import reg.tools as t
import reg.pnj as p
import data.loader as l

def main():
    "Procédure principale"
    ld = l.Loader("data/data.ini")

    # permet un affichage non-graphique
    if("-ng" in sys.argv):
        monPnj = p.Pnj(ld)
        lst = []
        for key in monPnj.carac:
            lst.append([key.replace('_',' '),monPnj.carac[key]])
        for e in lst:
            print(f"{e[0]} = {e[1]}")
    else:
        f.affichage(ld)

# si on lance via ligne de commande, on exécute la fonction main
if __name__ == "__main__":
    main()
