import discord
import asyncio
import os
import psycopg2
import random
import misc
import database

client = discord.Client()
prefix = '.'

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    miscobj = misc.Misc(client)
    database.establishConnection()
    await client.change_presence(game=random.choice(misc.games),afk=False)

def isCommand(message,command):
    return message.content.startswith(prefix+command)
        
@asyncio.coroutine
@client.event
async def on_message(message):
    if isCommand(message,'bestship'):
        await miscobj.bestship(message.channel)
    elif isCommand(message, 'updateusers'):
        await database.updateusers(message)
    elif isCommand(message, 'closedb'):
        await database.closedb(message.channel)
    elif isCommand(message, 'opendb'):
        await database.opendb(message.channel)
        
client.run(os.environ.get('BOT_TOKEN'))
