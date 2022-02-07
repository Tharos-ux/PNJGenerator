import discord
import reg.pnj as p
import re
import random
import csv
import datetime

def bot(ld):
    client = discord.Client()

    # préparation du dico de stress
    
    listStates,listEffects = [],[]
    with open("data/stress.csv", newline='') as reader:
        spamreader = csv.reader(reader, delimiter=',', quotechar='"')
        for l in spamreader:
            listStates.append(l[0])
            temp = l[1]
            listEffects.append(temp.replace('"',''))

    # mise en place de l'aide

    helps = {
                    "!sup":"pour obtenir de l'aide",
                    "!nom":"pour générer un nom aléatoire",
                    "!pnj":"pour générer un PnJ aléatoire",
                    "!jdr":"pour récupérer les liens utiles pour les séances",
                    "!links":"pour obtenir les liens vers les projets",
                    "!dX+Y/Z":"pour lancer un dé à X faces avec un bonus de Y sur une difficulté de Z",
                    "!sX":"pour lancer un dé de stress avec un stress de X",
                    "!meow":"Parce qu'il faut forcément un chat !"
                }
        
    help_string = "Vous pouvez utiliser les commandes :\n"
    for key,val in helps.items():
        help_string = help_string + f"\n**{key}** - *{val}*"

    @client.event
    async def on_ready():
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="les gens écrire !sup"))
        print(f"[{str(datetime.datetime.now())}] PNJMaker est prêt !")
        

    @client.event
    async def on_message(message):
        contents = message.content

        # nettoyage
        if(contents in ["!sup","!nom","!pnj","!meow","!jdr","!links","!ad"] or contents[:2] in ["!d","!s"]):
            print(f"[{str(datetime.datetime.now())}] Réception d'une commande de {str(message.author)} > {contents}")
            messages = await message.channel.history(limit=1).flatten()
            for each_message in messages:
                await each_message.delete()

        match contents:
            case "!ad":
                await message.channel.send("Hey ! C'est partiiiii !")
                e = discord.Embed(title="On est en live maintenant", url="https://www.twitch.tv/tharostv", description="Venez voir tout ce qu'on a pour vous !", color=0xF9BEE4)
                # e.set_thumbnail(url="https://media.discordapp.net/attachments/909452391244525598/939881649066369085/New_Logo_Color4.png")
                await message.channel.send(embed=e)

            case "!links":

                lembed =    [
                                discord.Embed(title="Youtube principal", url="https://www.youtube.com/channel/UCCn873wDjYSl_YZpNNTbViA", description="Les replays de JdR, les chroniques rôlistes et plein de formats funs", color=0xF9BEE4),
                                discord.Embed(title="Chaine de replays", url="https://www.youtube.com/channel/UCmmNBnYQmZlv6tPz6MO2TNA", description="Retrouvez ici tout ce que vous n'avez pas pu voir en live", color=0xF9BEE4),
                                discord.Embed(title="Streams twitch", url="https://www.twitch.tv/tharostv", description="Pour découvrir tout ce qu'on fait en live", color=0xF9BEE4),
                                discord.Embed(title="Github des projets", url="https://github.com/Tharos-ux", description="Pour récupérer des outils pour vos JdR", color=0xF9BEE4),
                                discord.Embed(title="Cycle de Niathshrubb", url="https://docs.google.com/document/d/1BC4PwwgtKJVfi3yFeJVzcIasZL3iVizx-WNH1jVvk9U/edit?usp=sharing", description="Pour découvrir ce que j'écris !", color=0xF9BEE4)
                            ]

                for e in lembed:
                    await message.channel.send(embed=e)

            case "!jdr":

                lembed =    [
                                discord.Embed(title="Règles des JdR", url="https://decorous-ptarmigan-9bf.notion.site/R-gles-JdR-ddd3ac0d4d0c4f98a9b2bcdd0d5cda79", description="Retrouvez ici l'intégralité des règles utilisées pendant les séances !", color=0xF9BEE4),
                                discord.Embed(title="Watch2Gether", url="https://w2g.tv/rooms/i0bpwst6mzv3t9qh9c7?access_key=vivvyyity2uburxwxo4wjm", description="Pour écouter la musique pendant les séances !", color=0xF9BEE4),
                                discord.Embed(title="Utilitaire pour les caméras", url="https://obs.ninja/", description="Pour les flux vidéos, si cela est nécessaire !", color=0xF9BEE4),
                                discord.Embed(title="GDoc du lore", url="https://docs.google.com/document/d/1Ytnvfar50VX2DmUkk1DoovrHz-nE_BAlFBGAkjkNX3Y/edit?usp=sharing", description="Rafraichissez-vous la mémoire quant au lore !", color=0xF9BEE4),
                                discord.Embed(title="Retours de séances", url="https://forms.gle/9nSjZwnFQChf9j546", description="Faites vos retours ici après la fin d'une série de JdR !", color=0xF9BEE4),
                                discord.Embed(title="S'inscrire pour une séance", url="https://forms.gle/TeEFqXFFJvKzvEEE7", description="Inscrivez-vous ici pour participer à une prochaine séance !", color=0xF9BEE4),
                                discord.Embed(title="Manuel de campagne : l'ombre du météore", url="https://decorous-ptarmigan-9bf.notion.site/Manuel-des-joueurs-l-ombre-du-m-t-ore-94bf941c54b54691971558724a154908", description="Par curiosité ou si vous êtes joueurs de la campagne !", color=0xF9BEE4)
                            ]

                for e in lembed:
                    await message.channel.send(embed=e)

            case '!sup': 

                await message.channel.send(help_string)

            case "!nom":

                string = p.Pnj(ld).name
                await message.channel.send(string)

            case "!pnj":

                monPnj,string = p.Pnj(ld),""
                for key in monPnj.carac:
                    string = string + f"**{key.replace('_',' ')}** = {monPnj.carac[key]}\n"
                await message.channel.send(string)

            case "!meow":

                await message.channel.send(file=discord.File('happy_cat.gif'))

            case _:

                if(contents[:2]=='!d'):

                    tvals = contents[2:].split('+')
                    vals = [tvals[0]] + tvals[1].split('/')
                    dice = random.randrange(1,int(vals[0]))
                    value = dice + int(vals[1])
                    if dice == 1:
                        quote = "La chance ne vous sourit pas toujours... et ce revers de fortune est cruel !"
                        state = "ECHEC CRITIQUE"
                    elif dice == int(vals[0]):
                        quote = "Brillant ! Pensez à rajouter votre point de statistique."
                        state = "REUSSITE CRITIQUE"
                    else:
                        if value>=int(vals[2]):
                            quote = random.choice(["Un coup décisif pour la chair comme pour l'esprit !","La voie est claire, le chemin dégagé : ne nous manque plus que la force pour l'emprunter."])
                            state = "REUSSITE"
                        else:
                            quote = random.choice(["Qui n'avait point prévu ces remuantes choses dans l'ombre ?","La vérité n'éclot jamais du mensonge.","A espoirs illusoires, rêves déchus !"])
                            state = "ECHEC"
                    string = f"{str(message.author).split('#')[0]} > **{state}**\n{dice}/{vals[0]} (dé) + {vals[1]} (bonus) = {value} pour une difficulté de {vals[2]}\n> *{quote}*"
                    print(string)
                    await message.channel.send(string)

                elif(contents[:2]=='!s'):

                    dice = random.randrange(1,10)
                    index = dice+int(contents[2:])
                    state = listStates[index]
                    effect = listEffects[index]
                    quote = "Pensez à ajuster votre cadre de stress !" if(dice >= 8 or dice <= 2) else "La vie n'est que coups au coeur et à l'esprit."
                    string = f"{str(message.author).split('#')[0]} > **{state}**\n{dice+1} (dé) : {effect}\n> *{quote}*"
                    print(string)
                    await message.channel.send(string)

    client.run("")
