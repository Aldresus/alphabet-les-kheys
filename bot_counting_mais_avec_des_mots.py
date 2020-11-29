import discord
from discord.ext import commands
from larousse_api import larousse
derniereLettre="`"
channel = 781464782414282813
points = 0
topNb=0
record=False
lienScoreboard='scoreboard.txt'
idBot=781488381719871510
# on part de ce caractère parce qu'on teste si la première lettre du mot entré par l'utilisateur est égale au code décimal de la dernière lettre + 1
# donc avec `+1 on obtient a

def embed(ctx): # non implémenté, l'objectif serait d'avoir un dictionnaire en complément de l'api (pour les anglicisme ou les mots de la street)
    embed=discord.Embed(title="**Aide:**", color=0xfcf794)
    embed.set_author(name="Alphabet les kheys")
    embed.add_field(name="**!mot [mot]** ", value="Commande pour ajouter un mot à la liste des mots autorisés.") # commande qui permettrait d'ajouter des mots.
    embed.set_footer(text="Made by Hugo | Aldresus with <3")
    return embed

def embedDef(ctx,definition): # joli affichage de la définition du mot entré (et valide)
    embed=discord.Embed(color=0x4d8bfe)

    embed.add_field(name="**{0}** ".format(ctx.content.capitalize()), value="{0}".format(definition)) # commande qui permettrait d'ajouter des mots.
    return embed

def embedFail(ctx,j): # joli affichage de la définition du mot entré (et valide)
    global points
    global record
    global topNb

    if record:
        embed=discord.Embed(title=":crown: **NOUVEAU RECORD !** :crown:",color=0xd29d00)
    else:
        embed=discord.Embed(color=0xff4013)

    embed.add_field(name='Vos points sont revenus à 0.',value="*Eh oui*",inline=False) # commande qui permettrait d'ajouter des mots.
    if points>1:
        embed.add_field(name="Score final :",value="**{0}** points.".format(points),inline=False)
    else:
        embed.add_field(name="Score final :",value="**{0}** point.".format(points),inline=False)
    if record:
        embed.add_field(name="Rank :",value="TOP 1 !!",inline=False)
    else:
        embed.add_field(name="Rank :",value="Top **{0}** sur **{1}**.".format(j-topNb+1,j),inline=False)
    return embed

def embedClassement(classement): # joli affichage de la définition du mot entré (et valide)
    embed=discord.Embed(color=0xfefcdd,title="10 Meilleurs records :")
    for i in range(len(classement)):
        if i >9 :
            break
        elif i==0:
            embed.add_field(name=":trophy: **{0}**er :".format(i+1), value="{0} points".format(classement[i]),inline=False)
        else:
            embed.add_field(name="**{0}**e :".format(i+1), value="{0} points".format(classement[i]),inline=True) # commande qui permettrait d'ajouter des mots.
    return embed

description = "Un bot qui t'apprends l'alphabet et étoffe ton langage."
client = commands.Bot(command_prefix='', description=description)
joueA="inventer des mots" #on défini le status qui est affiché

@client.event # debug
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name=joueA))

@client.event
async def on_message(ctx): # dès qu'un message est envoyé on stocke toutes ces infos (auteur, contenu, diverses ID, ...)+
    if channel==ctx.channel.id:
        global derniereLettre # on récupère la première lettre du dernier mot entré
        global points
        global record
        global topNb
        #role = discord.utils.get(ctx.guild.roles, name = "analphabète") #me donne les infos du role analphabète

        if ctx.author.id != idBot: # on vérifie que le bot ne s'auto réponde pas

            if ctx.content =="!aide": # si le message est la commande aide
                await ctx.channel.send(embed=embed(ctx),delete_after=20) # on affiche l'aide

            if ctx.content =="!top": # si le message est la commande aide
                classement=[]
                scoreboard=open(lienScoreboard,"r")
                for i in scoreboard :
                    classement.append(int(i.replace('\n','')))
                scoreboard.close
                classement.sort(reverse=True)
                await ctx.channel.send(embed=embedClassement(classement))


            elif "*" in ctx.content : # pour pouvoir parler sans que le bot ne s'énerve
                pass

            else :
                premiereLettre=ctx.content[0].replace("É","E").replace("é","e").lower() # on stocke la première lettre du mot en minuscule
                definition=larousse.get_definitions(ctx.content.lower()) # on récupère la définition du mot entré

                if ord(premiereLettre)!=ord(derniereLettre)+1: # si la première lettre du mot est bien celle qui suit la lettre stockée
                        await ctx.channel.send("Retourne apprendre l'alphabet {0} !".format(ctx.author.mention)) # on insulte si la réponse ne commence pas par la bonne lettre

                        scoreboard=open(lienScoreboard,"r")
                        j=0
                        for i in scoreboard :
                            j=j+1
                            i=i.replace('\n','')

                            if int(i)<=points :
                                topNb=topNb+1

                        scoreboard.close
                        if topNb==j:
                            record=True

                        await ctx.channel.send(embed=embedFail(ctx,j))

                        scoreboard=open(lienScoreboard,"a")
                        scoreboard.write("{0}\n".format(points))
                        scoreboard.close
                        points=0
                        topNb=0
                        record=False
                        derniereLettre="`"
                        # await ctx.author.add_role(role) censé give un role mais fonctionne po

                else :

                    if len(str(definition))>1000:
                        definition="La def est trop longue."

                    if definition!=[] : # si il n'y a pas de définition, on considère que le mot n'éxiste pas
                        await ctx.channel.send(embed=embedDef(ctx,str(definition).replace("[",'').replace("]",'').replace('"',''))) #on affiche la def pour rendre les gens + intélligents
                        await ctx.add_reaction('\N{THUMBS UP SIGN}') # on ajoute la réaction pouce vers le haut pour montrer que la réponse est bonne
                        derniereLettre=premiereLettre.lower() # on stocke la première lettre du mot pour la réutiliser plus tard
                        points=points+1 # on ajoute 1 pts

                        if derniereLettre=="z": # si on est à la lettre z
                            derniereLettre="`" # on retourne à a
                            await ctx.channel.send("BRAVO :partying_face: ! Vous venez de completer l'alphabet ! On repart de 'A'".format(ctx.author.mention))

                    else :
                        await ctx.channel.send("Ça veut rien dire {0} !".format(ctx.author.mention)) #on insulte si le mot entré n'est pas reconnu
                        # await ctx.author.add_role(role) censé give un role mais fonctionne po

client.run('Token du bot')
