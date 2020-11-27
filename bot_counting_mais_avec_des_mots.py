import discord
from discord.ext import commands
from larousse_api import larousse

derniereLettre="`"
channel = 781464782414282813
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
        role = discord.utils.get(ctx.guild.roles, name = "analphabète") #me donne les infos du role analphabète

        if derniereLettre=='z': # si on est à la lettre z
            derniereLettre="`" # on retourne à a

        if ctx.author.id != 781488381719871510: # on vérifie que le bot ne s'auto réponde pas

            if ctx.content =="!aide": # si le message est la commande aide
                await ctx.channel.send(embed=embed(ctx),delete_after=20) # on affiche l'aide

            elif "*" in ctx.content : # pour pouvoir parler sans que le bot ne s'énerve
                pass

            else :
                definition=larousse.get_definitions(ctx.content.lower()) # on récupère la définition du mot entré
                print(ctx.content) # debug
                print(definition) # debug

                if definition==[] : # si il n'y a pas de définition, on considère que le mot n'éxiste pas
                    await ctx.channel.send("Ça veut rien dire {0} !".format(ctx.author.mention)) #on insulte si le mot entré n'est pas reconnu
                    # await ctx.author.add_role(role) censé give un role mais fonctionne po

                else :
                    premiereLettre=ctx.content[0].lower() # on stocke la première lettre du mot en minuscule
                    print(premiereLettre)

                    if ord(premiereLettre)==ord(derniereLettre)+1: # si la première lettre du mot est bien celle qui suit la lettre stockée
                        await ctx.channel.send(embed=embedDef(ctx,str(definition).replace("[",'').replace("]",'').replace('"',''))) #on affiche la def pour rendre les gens + intélligents
                        await ctx.add_reaction('\N{THUMBS UP SIGN}') # on ajoute la réaction pouce vers le haut pour montrer que la réponse est bonne
                        derniereLettre=premiereLettre.lower() # on stocke la première lettre du mot pour la réutiliser plus tard

                    else :
                        await ctx.channel.send("Retourne apprendre l'alphabet {0} !".format(ctx.author.mention)) # on insulte si la réponse ne commence pas par la bonne lettre
                        # await ctx.author.add_role(role) censé give un role mais fonctionne po
    else:
        print("autre channel")


client.run('Token du bot')