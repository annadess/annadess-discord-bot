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

@asyncio.coroutine
@client.event
async def on_message(message):
    if message.content.startswith(prefix+'test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith(prefix+'sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')
	elif message.content.startswith(prefix+'bestship'):
		await client.send_message(message.channel, 'Kuno x Wyn is definitely the best ship')
		

client.run(os.environ.get('BOT_TOKEN'))
