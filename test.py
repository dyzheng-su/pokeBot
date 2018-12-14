# Work with Python 3.6
# Diana Zheng
# Xueyu Zhang
import requests
import discord
import random
import asyncio
import aiohttp
import json
import pokebase as pb
from discord import Game
from discord.ext.commands import Bot

#global variable

BOT_PREFIX = ("!")
AUTHOR = 'PokeBot'
TOKEN = ""
FOOTER=''
MAX = 6
WILD_MON = ''
CATCHED = False
USERS = {}
base_mons = ['bulbasaur', 'charmander', 'squirtle', 'chikorita', 'cyndaquil', 'totodile', 'treecko',
        'torchic', 'mudkip', 'turtwig', 'chimchar', 'piplup', 'snivy', 'tepig', 'oshawott', 'chespin', 'fennekin', 
        'froakie', 'rowlet', 'litten', 'popplio']


# Create an POKE_USER object for each user
# Produced by Xueyu Zhang
class POKE_USER:
    win_rate = 0.0
    win_times = 0
    battle_times = 0
    count = 0
    #selected_pokemon = None

    def __init__(self, username, pokemon_list=None):
        if pokemon_list is None:
            pokemon_list = {}
        self.username = username
        self.pokemon_list = pokemon_list

# Create an POKEMON object
# Produced by Xueyu Zhang
class POKEMON:
    level = 1
    battle_times = 0
    battle_percent = 0.0
    win_times = 0
    win_rate = 0.0

    def __init__(self, name):
        self.name = name


client = Bot(command_prefix=BOT_PREFIX) 


# This command has to go first before a user join the game.
# Will create an account for the user.
# Produced by Xueyu Zhang
@client.command(pass_context=True)
async def start(ctx):
    new_user = ctx.message.author.name
    print(new_user)
    i=0
    base_list = ''
    if new_user in USERS: 
        print("yes")
        await client.say("%s already started!" % new_user)
        return
    else:
        USERS[new_user] = POKE_USER(new_user)
        print("pokemon_list: ", USERS[new_user].pokemon_list)
        while i < len(base_mons):
            base_list += (base_mons[i].capitalize() + '|')
            i += 1
            if not i%3: base_list += '\n'
            
        embed = discord.Embed(
            title = 'Choose a base pokemon to start your adventure!', 
            description = base_list
        )
        embed.set_footer(text="type !pick to pick your first pokemon")
        embed.set_author(name=AUTHOR
            #,icon_url=
        )
        await client.say(embed=embed)

        # When the game started, wild pokemons will appeared randomly
        while 1:
            rand_time = random.randrange(50,100)
            await asyncio.sleep(rand_time)
            await wild_pokemon()



# @client.command(pass_context=True)
# async def select(ctx):
#     context = ctx.message.content.split()[1].lower()
#     user = USERS[ctx.message.author.name]
#     pl = user.pokemon_list

#     new_select_mon = pl.get(context,0)
#     if new_select_mon:
#         user.selected_pokemon = new_select_mon
#         embed = discord.Embed(
#         title = '%s select %s' % (user.username, context), 
#         description = base_list
#         )
#         embed.set_footer(text=FOOTER)
#         embed.set_author(name=AUTHOR
#         #,icon_url=
#         )
#         await client.say(embed=embed)
#     else:
#         embed = discord.Embed(
#         title = '%s can not select %s, type !info to check pokemon list' % (user.username, context), 
#         description = base_list
#         )
#         embed.set_footer(text=FOOTER)
#         embed.set_author(name=AUTHOR
#         #,icon_url=
#         )
#         await client.say(embed=embed)


# When the user join the game, he/she must pick a base pokemon
# Users already had a base pokemon are not allowed to pick again
# Produced by Xueyu Zhang
@client.command(pass_context=True)
async def pick(ctx):
    new_user = ctx.message.author.name
    mon = ctx.message.content.split()[1].lower()
    print(mon)
    if new_user not in USERS:
        await client.say("type !start to create your account first")
    else:
        user = USERS[new_user]
        if user.count > 0:
            await client.say("%s already picked a base pokemon" % new_user)
        else: 
            if mon in base_mons:
                msg = "Good luck! %s and your pokemon %s" % (new_user, mon)
                pl = user.pokemon_list
                new_pokemon = POKEMON(mon)
                pl[mon] = new_pokemon
                USERS[new_user].count += 1
                await client.say(msg)
            else:
                await client.say(("%s is not a base pokemon" % mon))


# To look up a user's infomation
# if there is no username input, then user will see his/her own information
# Only users who have started the game can be seen.
# Produced by Xueyu Zhang
@client.command(pass_context=True)
async def info(ctx):
    context = ctx.message.content.split()
    if len(context) > 1:
        username = context[1]
    else:
        username = ctx.message.author.name
    if username in USERS:
        user = USERS[username]
        pl = user.pokemon_list
        des = ('pokemons %d | total battles %d | total win %d | win percent %.2f\n\n\n') % (user.count, user.battle_times, user.win_times, user.win_rate)
        for name in pl:
            des += ('%s | level %d | battle times %d | battle percent %2.f | win times %d | win rate %.2f\n') % (pl[name].name, 
                pl[name].level, pl[name].battle_times, pl[name].battle_percent, pl[name].win_times, pl[name].win_rate)

        embed = discord.Embed(
            title = ('%s\'s infomation') % username,
            description = des
        )

        embed.set_footer(text=FOOTER)
        embed.set_author(name=AUTHOR
            #,icon_url=
        )
        await client.say(embed=embed)

    else:
        await client.say("%s has not created an account yet")


# When a wild random pokemon occurs, users are able to catch it
# However, only the first one who execute this command can catch it.
# If a user reach the maximum number of pokemon (6) one can have, he/she can not catch it
# Produced by Xueyu Zhang
@client.command(pass_context=True)
async def catch(ctx):
    global CATCHED
    if ctx.message.author.name not in USERS:
        await client.say("type !start to create your account first")
    else:
        if CATCHED: 
            await client.say("%s has been caught!" % WILD_MON)
        else:
            user = USERS[ctx.message.author.name]
            if WILD_MON in user.pokemon_list:
                await client.say("%s already had a %s" % (user.username, WILD_MON))
            elif user.count == MAX: 
                await client.say("%s already has 6 pokemon.\n type !release to release a pokemon" % user.username)
            else:
                new_pokemon = POKEMON(WILD_MON)
                user.pokemon_list[WILD_MON] = new_pokemon
                user.count += 1
                await client.say('%s caught this wild %s' % (user.username, WILD_MON))
                CATCHED = True

# A user can release a pokemon that currently in his/her list
# Produced by Xueyu Zhang
@client.command(pass_context=True)
async def release(ctx):
    context = ctx.message.content.split()
    if len(context) == 1:
        await client.say("Please specify the pokemon that you want to release")
        return
    user = ctx.message.author.name 
    if user not in USERS:
        await client.say("type !start to create your account first")
    else:
        pl = USERS[user].pokemon_list
        mon = context[1]
        if mon not in pl:
            await client.say("%s does not have a %s \n type !info to check your list" % (user, mon))
        else:
            pl.pop(mon)
            USERS[user].count -= 1
            await client.say("%s has released a %s" % (user, mon))


# Lookup a pokemon information
# No need to create an account first.
# Produced by Xueyu Zhang
@client.command(pass_context=True)
async def lookup(ctx):
    ct = ctx.message.content.split()
    if len(ct) == 1: 
        await client.say("Please specify the pokemon's name")
        return
    if len(ct) > 2: 
        await client.say("Too many inputs")
        return
    content = ct[1].lower()
    try:
        mons = pb.pokemon(content)
        embed = discord.Embed(
            title = mons.name.capitalize()
        )
        embed.set_footer(text=FOOTER)
        embed.set_image(url=mons.sprites.front_default)
        embed.set_author(name=AUTHOR
            #,icon_url=
        )
        #embed.set_thumbnail
        embed.add_field(name='Species', value=mons.species.name, inline=True)
        #embed.add_field(name='Habitat', value=mons.species.habitat.name, inline=True)
        embed.add_field(name='Base experience', value=mons.base_experience, inline=True)
        embed.add_field(name='Id', value=mons.id, inline=True)
        embed.add_field(name='Height', value=mons.height, inline=True)
        embed.add_field(name='Weight', value=mons.weight, inline=True)
        for stat in mons.stats:
            embed.add_field(name=stat.stat.name.capitalize(), value=stat.effort, inline=True)

        abilities = ''
        for ability in mons.abilities:
            abilities += (ability.ability.name + ' | ')

        embed.add_field(name='Ability', value=abilities, inline=True)

        await client.say(embed=embed)
    except:
        await client.say("%s is not a pokemon" % content)





@client.command(pass_context=True)
async def battle(ctx):
    context = ctx.message.content.split()


    # A helper function to return the member's display name
    member = ctx.message.server.get_member_named(context[1])
    challenger = ctx.message.author.name
    if challenger not in USERS or context[1] not in USERS:
        await client.say("Both players must have an account first.\nType !start to create your account!")
    elif len(context) < 3:
        await client.say("Please enter in the Player you wish to battle and the pokemon you wish to battle them.")
    else:
        poke = context[2].lower()
        if poke not in USERS[challenger].pokemon_list:
            await client.say("You do not have a %s" % poke)
        else:
            await client.say(member.mention + "You have been challenged!" ) 

            poke = context[2].lower()
            mons = pb.pokemon(poke)
            embed = discord.Embed(
                title = (challenger + " has challenged you with " +mons.name.capitalize() + "!")
            )
            embed.set_image(url=mons.sprites.front_default)
            await client.say(embed=embed)   

            response = await client.wait_for_message(author=member, timeout=30)

            if response is None:
                await client.say("%s did not respond. Battle canceled." % context[1])
                return
                # USERS[context[1]].battle_times +=1
                # USERS[challenger].battle_times +=1
                # USERS[context[1]].win_rate = USERS[context[1]].win_times / USERS[context[1]].battle_times
                # USERS[challenger].win_rate = USERS[challenger].win_times / USERS[challenger].battle_times
            else:    
                challenged_poke = response.content.lower()
                if challenged_poke not in USERS[context[1]].pokemon_list:
                    await client.say("You do not have a %s. Battle interrupted." % challenged_poke)
                else:
                    challenged_mon = pb.pokemon(challenged_poke)
                    embed2 = discord.Embed(
                        title = (str(member) + " has used " + challenged_mon.name.capitalize() + "!")
                    )
                    embed2.set_image(url=challenged_mon.sprites.front_default)
                    await client.say(embed=embed2)  

                    USERS[context[1]].battle_times +=1
                    USERS[challenger].battle_times +=1  

                    update_pokemon(context[1],challenged_poke)
                    update_pokemon(challenger,poke) 

                    if battle_stats(mons, challenged_mon) == 1:
                        winner = challenger
                        url=mons.sprites.front_default
                        USERS[winner].win_times += 1
                        USERS[winner].win_rate = USERS[winner].win_times / USERS[winner].battle_times
                        inc_pokemon(challenger, poke)   

                    elif battle_stats(mons, challenged_mon) == 2:
                        winner = context[1]
                        url=challenged_mon.sprites.front_default
                        USERS[winner].win_times += 1
                        USERS[winner].win_rate = USERS[winner].win_times / USERS[winner].battle_times
                        inc_pokemon(context[1], challenged_poke)    

                    else:
                        winner =  "Draw!"
                        pikachu = pb.pokemon("pikachu")
                        url=pikachu.sprites.front_default    
                    winningEmbed = discord.Embed(
                        title = ("Winner: "+ winner))
                    winningEmbed.set_image(url=url)
                        
                    await client.say(embed = winningEmbed)  

            

def inc_pokemon(player, mon):
    user = USERS[player]
    pl = user.pokemon_list
    if mon in pl:
        pl[mon].battle_percent = pl[mon].battle_times / user.battle_times
        pl[mon].win_times += 1
        pl[mon].win_rate = pl[mon].win_times / pl[mon].battle_times
            
def update_pokemon(player, mon):
    user = USERS[player]
    pl = user.pokemon_list
    if mon in pl:
        pl[mon].battle_times +=1
        pl[mon].battle_percent = pl[mon].battle_times / user.battle_times
        pl[mon].win_rate = pl[mon].win_times / pl[mon].battle_times
            

def battle_stats(p1, p2):
    p2stats = p2.base_experience

    for stat in p2.stats:
        if (stat.stat.name != "Weight") and (stat.stat.name != "Defense") and (stat.stat.name != "Special-defense"):
            p2stats += stat.effort

    p1stats = p1.base_experience

    for stat in p1.stats:
        if stat.stat.name != "Weight" and stat.stat.name != "Defense" and stat.stat.name != "Special-defense":
            p1stats += stat.effort

    r1 = random.randrange(5,10)
    r2 = random.randrange(5,10)

    p1stats, p2stats = p1stats * r1, p2stats * r2

    if p1stats > p2stats:
        return 1
    elif p2stats > p1stats:
        return 2
    else:
        return 0



# @client.command(pass_context=True)
# async def moves(ctx):
#     content = ctx.message.content.split()[1].lower()
#     pokemon = pb.pokemon(content)
#     pokemon_moves = ''
#     i = 0
#     for move in pokemon.moves:
#         #if move.version_group_details[0]['version_group']['name'] == 'omega-ruby-alpha-sapphire':
#         pokemon_moves += '%s | ' % (move.move.name)
#         i += 1
#         if not i%5: pokemon_moves += '\n'

    
#     embed = discord.Embed(
#         title = ('%s\'s moves' % (content.capitalize())),
#         description = pokemon_moves
#     )
#     #embed.set_footer(text=FOOTER)
#     embed.set_author(name=AUTHOR,
#         #,icon_url
#     )
#     await client.say(embed=embed)



# Generated a random wild pokemon with the API
# invoked in pick() function
# Produced by Xueyu Zhang
async def wild_pokemon():
    global WILD_MON, CATCHED

    url = "https://pokeapi.co/api/v2/pokemon/"
    response = requests.get(url)
    data = response.json()
    total = data['count']
    rand = random.randrange(total)
    wild = data['results'][rand]['name']

    WILD_MON = wild
    CATCHED = False

    wild_mon = pb.pokemon(wild)
    embed = discord.Embed(
        title = wild_mon.name.capitalize(),
        description = "A wild %s appears!!" % wild_mon.name.capitalize()
    )
    embed.set_footer(text="type !catch to catch this wild %s" % wild)
    embed.set_image(url=wild_mon.sprites.front_default)
    embed.set_author(name=AUTHOR
        #,icon_url=
    )
    #embed.set_thumbnail
    embed.add_field(name='Species', value=wild_mon.species.name, inline=True)
    #embed.add_field(name='Habitat', value=wild_mon.species.habitat.name, inline=True)
    embed.add_field(name='Base experience', value=wild_mon.base_experience, inline=True)
    embed.add_field(name='Id', value=wild_mon.id, inline=True)
    for stat in wild_mon.stats:
        embed.add_field(name=stat.stat.name.capitalize(), value=stat.effort, inline=True)
    abilities = ''
    for ability in wild_mon.abilities:
        abilities += (ability.ability.name + ' | ')

    embed.add_field(name='Ability', value=abilities, inline=True)

    await client.say(embed=embed)


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(60)



client.loop.create_task(list_servers())
client.run(TOKEN)