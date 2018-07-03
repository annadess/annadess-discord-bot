import discord
import asyncio
import os
import psycopg2
import random
import misc
import database
import userlogic

client = discord.Client()
prefix = '.'
miscobj = misc.Misc(client)
dataobj = database.Database(client)
userlogic = userlogic.UserLogic(client,dataobj)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=random.choice(miscobj.games),afk=False)

def isCommand(message,command):
    return message.content.startswith(prefix+command)
        
@asyncio.coroutine
@client.event
async def on_message(message):
    if isCommand(message,'bestship'):
        await miscobj.bestship(message.channel)
    elif isCommand(message, 'updateusers'):
        await userlogic.updateusers(message)
    elif isCommand(message, 'closedb'):
        await dataobj.closedb(message.channel)
    elif isCommand(message, 'opendb'):
        await dataobj.opendb(message.channel)
    elif isCommand(message, 'newgame'):
        await miscobj.newgame()
    elif isCommand(message, 'runsql'):
        await dataobj.runsql(message)
    elif 'gay'.upper() in message.content.upper() and 'connor'.upper() in message.content.upper():
        await miscobj.bromance(message.channel)
        
client.run(os.environ.get('BOT_TOKEN'))
