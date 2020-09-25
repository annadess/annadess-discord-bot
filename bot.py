import discord
from discord.ext import commands
import asyncio
import os
import psycopg2
import random
import misc
import database
import userlogic

client = commands.Bot(command_prefix='.')
miscobj = misc.Misc(client)
dataobj = database.Database(client)
userlogic = userlogic.UserLogic(client,dataobj)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    #await client.change_presence(game=random.choice(miscobj.games),afk=False)

@client.command()
async def test(ctx, description="Test"):
	await miscobj.bestship(ctx)
	
	
#def isCommand(message,command):
#    return message.content.startswith(prefix+command)
        
#@asyncio.coroutine
#@client.event
#async def on_message(message):
#    if isCommand(message,'bestship'):
#        await miscobj.bestship(message.channel)
#    elif isCommand(message, 'updateusers'):
#        await userlogic.updateusers(message)
#    elif isCommand(message, 'closedb'):
#        await dataobj.closedb(message.channel)
#    elif isCommand(message, 'opendb'):
#        await dataobj.opendb(message.channel)
#    elif isCommand(message, 'newgame'):
#        await miscobj.newgame()
#    elif isCommand(message, 'runsql'):
#        await dataobj.runsql(message)
#    elif 'gay'.upper() in message.content.upper() and 'connor'.upper() in message.content.upper():
#        await miscobj.bromance(message.channel)
#    elif isCommand(message, 'mybirthday'):
#        await userlogic.mybirthday(message)
#    elif isCommand(message, 'nextbirthdays'):
#        await userlogic.nextbirthdays(message.channel)
#    elif isCommand(message, 'help hu'):
#        await miscobj.helphu(message.channel)
#    elif isCommand(message, 'help'):
#        await miscobj.helpen(message.channel)
        
client.run(os.environ.get('BOT_TOKEN'))
