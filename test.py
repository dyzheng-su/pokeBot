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

BOT_PREFIX = ("!")
AUTHER = 'PokeBot'
TOKEN = ""
FOOTER = 'This is a footer'
WILD_MON = 'XXXXXXXXXXXXXXXXXXX'
USERS = {}
pick_user = ''
catch_user = ''
select_user = ''
base_mons = ['bulbasaur', 'charmander', 'squirtle', 'chikorita', 'cyndaquil', 'totodile', 'treecko',
        'torchic', 'mudkip', 'turtwig', 'chimchar', 'piplup', 'snivy', 'tepig', 'oshawott', 'chespin', 'fennekin', 
        'froakie', 'rowlet', 'litten', 'popplio']



class POKE_USER:

    pokemon_list = {}
    win_rate = 0.0
    win_times = 0
    battle_times = 0
    count = 0

    def __init__(self, username, base_pokemon):
        self.username = username
        self.selected_pokemon = POKEMON(base_pokemon)
        self.pokemon_list[base_pokemon] = self.selected_pokemon
        self.count += 1

    def select(self, pokemon):
        if pokemon in pokemon_list:
            self.selected_pokemon = self.pokemon_list[pokemon]
            self.selected_pokemon.battle_percent = self.selected_pokemon.battle_times / self.battle_times


class POKEMON:
    level = 1
    battle_times = 0
    battle_percent = 0.0
    win_times = 0
    win_rate = 0.0

    def __init__(self, name):
        self.name = name


client = Bot(command_prefix=BOT_PREFIX) 


# @client.command()
# async def battle(player):


# @client.command()
# async def ranking():



@client.command()
async def start():
    i=0
    base_list = ''
    while i < len(base_mons):
        base_list += (base_mons[i].capitalize() + '|')
        i += 1
        if not i%3: base_list += '\n'
        
    embed = discord.Embed(
        title = 'Choose a base pokemon to start your adventure!', 
        description = base_list
    )
    embed.set_footer(text="type !pick to pick your first pokemon")
    embed.set_author(name=AUTHER
        #,icon_url=
    )

    await client.say(embed=embed)


@client.command()
async def select(context):
    context = context.lower()
    user = USERS[select_user]
    pl = user.pokemon_list

    new_select_mon = pl.get(context,0)
    if new_select_mon:
        user.selected_pokemon = new_select_mon
        embed = discord.Embed(
        title = '%s select %s' % (user.username, context), 
        description = base_list
        )
        embed.set_footer(text=FOOTER)
        embed.set_author(name=AUTHER
        #,icon_url=
        )
        await client.say(embed=embed)
    else:
        embed = discord.Embed(
        title = '%s can not select %s, type !info to check pokemon list' % (user.username, context), 
        description = base_list
        )
        embed.set_footer(text=FOOTER)
        embed.set_author(name=AUTHER
        #,icon_url=
        )
        await client.say(embed=embed)



@client.command()
async def pick(message):
    mon = message.lower()
    if mon in base_mons:
        msg = "Good luck! %s and your pokemon %s" % (pick_user, mon)
        new_user = POKE_USER(pick_user,mon)
        USERS[pick_user] = new_user
        await client.say(msg)
    else:
        await client.say(("%s is not a base pokemon" % mon))

    while 1:
        rand_time = random.randrange(200,500)
        await asyncio.sleep(rand_time)
        await wild_pokemon()

@client.command()
async def info(context):
    user = USERS[context]
    pl = user.pokemon_list
    des = ('pokemons %d | total battles %d | total win %d | win percent %d\n\n\n') % (user.count, user.battle_times, user.win_times, user.win_rate)
    for name in pl:
        des += ('%s | level %d | battle times %d | battle percent %d | win times %d | win rate %d\n') % (pl[name].name, 
            pl[name].level, pl[name].battle_times, pl[name].battle_percent, pl[name].win_times, pl[name].win_rate)

    embed = discord.Embed(
        title = ('%s\'s infomation') % context,
        description = des
    )

    embed.set_footer(text=FOOTER)
    embed.set_author(name=AUTHER
        #,icon_url=
    )

    await client.say(embed=embed)


@client.command()
async def catch():
    new_pokemon = POKEMON(WILD_MON)
    USERS[catch_user].pokemon_list[WILD_MON] = new_pokemon
    await client.say('type !info to check your new pokemons')

    


#Simple pokemon look up command. Is working correctly. Need to find more interactionsw ith it.
@client.command()
async def lookup(context):
    context = context.lower()
    mons = pb.pokemon(context)
    embed = discord.Embed(
        title = mons.name.capitalize()
    )
    embed.set_footer(text=FOOTER)
    embed.set_image(url=mons.sprites.front_default)
    embed.set_author(name=AUTHER
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



@client.command()
async def moves(context):
    context = context.lower()
    pokemon = pb.pokemon(context)
    pokemon_moves = ''
    i = 0
    for move in pokemon.moves:
        #if move.version_group_details[0]['version_group']['name'] == 'omega-ruby-alpha-sapphire':
        pokemon_moves += '%s | ' % (move.move.name)
        i += 1
        if not i%5: pokemon_moves += '\n'

    
    embed = discord.Embed(
        title = ('%s\'s moves' % (context.capitalize())),
        description = pokemon_moves
    )
    #embed.set_footer(text=FOOTER)
    embed.set_author(name=AUTHER,
        #,icon_url
    )

    await client.say(embed=embed)


async def wild_pokemon():
    global WILD_MON

    url = "https://pokeapi.co/api/v2/pokemon/"
    response = requests.get(url)
    data = response.json()
    total = data['count']
    rand = random.randrange(total)
    wild = data['results'][rand]['name']

    WILD_MON = wild

    wild_mon = pb.pokemon(wild)
    embed = discord.Embed(
        title = wild_mon.name.capitalize(),
        description = "A wild %s appears!!" % wild_mon.name.capitalize()
    )
    embed.set_footer(text="type !catch to catch this wild %s" % wild)
    embed.set_image(url=wild_mon.sprites.front_default)
    embed.set_author(name=AUTHER
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


@client.event
async def on_message(message):
    global pick_user, catch_user, select_user
    if message.author == client.user:
        return

    if message.content.startswith('!pick'):
        pick_user = message.author.name

    if message.content.startswith('!catch'):
        catch_user = message.author.name

    if message.content.startswith('!select'):
        select_user = message.author.name

    await client.process_commands(message)

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(60)



client.loop.create_task(list_servers())
client.run(TOKEN)