# Work with Python 3.6
# Diana Zheng
# Xueyu Zhang
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
TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
users = {}
FOOTER = 'This is a footer'
user = ''


client = Bot(command_prefix=BOT_PREFIX) 


@client.command()
async def start():
    base_mons = ['bulbasaur', 'charmander', 'squirtle', 'chikorita', 'cyndaquil', 'totodile', 'treecko',
        'torchic', 'mudkip', 'turtwig', 'chimchar', 'piplup', 'snivy', 'tepig', 'oshawott', 'chespin', 'fennekin', 
        'froakie', 'rowlet', 'litten', 'popplio'
    ]
    
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
    embed.set_footer(text=FOOTER)
    embed.set_author(name=AUTHER
        #,icon_url=
    )

    await client.say(embed=embed)


@client.command()
async def pick(message):
    print(message)


@client.command()
async def list():
    pokemon_list = users[user]['pokemon_list']
    des = ''
    for pokemon in pokemon_list:
        des += ('%s|  level %d\n') % (pokemon['name'], pokemon['level'])

    embed = discord.Embed(
        title = ('%s\'s pokemons') % user,
        description = des
    )

    embed.set_footer(text=FOOTER)
    embed.set_author(name=AUTHER
        #,icon_url=
    )

    await client.say(embed=embed)


@client.command()
async def catch(context):
    context = context.lower()
    users[user]['pokemon_list'].append({'name': context, 'level': 0})
    await client.say('type !list to check your new pokemons')

    


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
    embed.set_footer(text=FOOTER)
    embed.set_author(name=AUTHER,
        #,icon_url
    )

    await client.say(embed=embed)


@client.event
async def on_message(message):
    global user, users
    if message.author == client.user:
        return

    if message.content.startswith('!pick'):
        mon = (message.content.split())[1].lower()
        msg = "Good luck! %s and your pokemon %s" % (message.author.name, mon)
        pokemon_list = [{'name': mon, 'level': 0}]
        pokemons = {'pokemon_list': pokemon_list, 'selected_pokemon': mon}
        user = message.author.name
        users[user] = pokemons
        await client.send_message(message.channel, msg)

    if message.content.startswith('!list'):
        user = message.author.name
    

    if message.content.startswith('!catch'):
        user = message.author.name

    await client.process_commands(message)




async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)