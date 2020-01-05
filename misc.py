import discord
import asyncio
import os
import psycopg2
import random

class Misc:

    def __init__(self, client):
        self.client = client
        
    games = [discord.Game(name="detective",type=0),
discord.Game(name="with Sumo",type=0),
discord.Game(name="the android sent by CyberLife",type=0),
discord.Game(name="baseball with Hank",type=0),
discord.Game(name="wake up Lieutenant",type=0),
discord.Game(name="your buddy to drink with",type=0),
discord.Game(name="blowing up Jericho",type=0)]
    
    @asyncio.coroutine
    async def bestship(self,channel):
        await self.client.send_message(channel, 'Sir, the Kuno and Wyn pairing, is undoubtedly, the best pairing in this currently running role playing game.')
        
    @asyncio.coroutine
    async def newgame(self):
        await self.client.change_presence(game=random.choice(self.games),afk=False)
        
    @asyncio.coroutine
    async def bromance(self,channel):
        await self.client.send_message(channel, 'I\'m certainly going to miss our bromance.')

    @asyncio.coroutine
    async def helpen(self,channel):
        await self.client.send_message(channel, """```Multi
Line
Test```""")
                                 
    @asyncio.coroutine
    async def helphu(self,channel):
        await self.client.send_message(channel, """```Többsoros
Teszt```""")
