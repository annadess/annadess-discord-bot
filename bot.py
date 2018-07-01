import discord
import asyncio
import os

client = discord.Client()
prefix = ','
f=open("file.txt","w+")
f.close()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def isCommand(message,command):
    return message.content.startswith(prefix+command)
    
@asyncio.coroutine
@client.event
async def on_message(message):
    if isCommand(message,'bestship'):
        await client.send_message(message.channel, 'Kuno x Wyn is definitely the best ship')
    elif isCommand(message, 'writefile'):
        with open("file.txt") as file:
            f.write("sample")
            await client.send_message(message.channel, 'written to file')
    elif isCommand(message, 'readfile'):
        with open("file.txt") as file:
            content = f.read("sample")
            await client.send_message(message.channel, content)        

client.run(os.environ.get('BOT_TOKEN'))
