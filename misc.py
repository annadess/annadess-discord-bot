import discord
import asyncio
import os
import psycopg2
import random

class Misc(client):
    games = [discord.Game(name="detective",type=0),
discord.Game(name="with Sumo",type=0),
discord.Game(name="the android sent by CyberLife",type=0),
discord.Game(name="baseball with Hank",type=0),
discord.Game(name="wake up Lieutenant",type=0),
discord.Game(name="your buddy to drink with",type=0),
discord.Game(name="blowing up Jericho",type=0)]
    
    client = client
    
    @asyncio.coroutine
    async def bestship(channel):
        await client.send_message(channel, 'Sir, the Kuno and Wyn pairing, is undoubtedly, the best pairing in this currently running role playing game.')

