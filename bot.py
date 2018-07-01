import discord
import asyncio
import os

client = discord.Client()
prefix = ','

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def isCommand(message, command):
    return message.content.startswith(prefix+message)
    
@asyncio.coroutine
@client.event
async def on_message(message):
    if isCommand(message,'bestship'):
        await client.send_message(message.channel, 'Kuno x Wyn is definitely the best ship')

client.run(os.environ.get('BOT_TOKEN'))
