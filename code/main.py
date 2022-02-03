#!/usr/bin/python3.10

import sys
import os
import ife.interface as f
import reg.regexpr as r
import reg.tools as t
import reg.pnj as p
import data.loader as l
import discord

def main():
    "Procédure principale"
    liste_dicos = dict()
    directory_in_str = "data/sdd/"
    directory = os.fsencode(directory_in_str)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".ini"):
            liste_dicos[filename] = l.Loader(f"{directory_in_str}{filename}")
    # dico par défaut
    ld = liste_dicos[list(liste_dicos.keys())[0]] if liste_dicos != dict() else l.Loader("data/data.ini")

    client = discord.Client()
    client.run("")

    @client.event
    async def on_ready():
        print("Le bot est prêt !")

    @client.event
    async def on_message(message):
        print(message.content)
        if message.content == 'Pnj':
            await message.channel.send(p.Pnj(ld))

    # permet un affichage non-graphique
    if("-ng" in sys.argv):
        monPnj = p.Pnj(ld)
        lst = []
        for key in monPnj.carac:
            lst.append([key.replace('_',' '),monPnj.carac[key]])
        for e in lst:
            print(f"{e[0]} = {e[1]}")
    else:
        f.affichage(ld,liste_dicos)

# si on lance via ligne de commande, on exécute la fonction main
if __name__ == "__main__":
    main()
