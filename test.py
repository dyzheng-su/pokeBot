# Work with Python 3.6
# Diana Zheng
# Xueyu Zhang

import random
import asyncio
import aiohttp
import json
import pokebase as pb
from discord import Game
from discord.ext.commands import Bot

BOT_PREFIX = ("!")
TOKEN = "NTE4MjM4NTgwMjA0NzY1MjA2.DuN3oQ.usZM4dEaC9ht2NEPdAmWFJiZN4A"  
## Token from specific bot, need to switch token when trying on different accounts.

client = Bot(command_prefix=BOT_PREFIX) 

## Code from the internet as an example of what the bot can do.
@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)



@client.command()
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))

#Simple pokemon look up command. Is working correctly. Need to find more interactionsw ith it.
@client.command()
async def lookup(context):
    mons = pb.pokemon(context)
    print(mons)
    await client.say("the pokemon's height is: " + str(mons.location_area_encounters))

#Progress of writing and saving information to files. So far, stuff is being written down.
#Should keep a dict format and store rankings w/ keys + values.
@client.command()
async def save(context):
    with open('text.txt','a+') as file:
        file.write(context + "\n")
        await client.say("Your message was saved: " + context)


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)


@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)