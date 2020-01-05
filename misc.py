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
        await self.client.send_message(channel, 'Sir, the Kuno and Wyn pairing, is undoubtedly, the best pairing out of all of them.')
        
    @asyncio.coroutine
    async def newgame(self):
        await self.client.change_presence(game=random.choice(self.games),afk=False)
        
    @asyncio.coroutine
    async def bromance(self,channel):
        await self.client.send_message(channel, 'I\'m certainly going to miss our bromance.')

    @asyncio.coroutine
    async def helpen(self,channel):
        await self.client.send_message(channel, """```
Commands:
bestship - Connor's opinion on the best ship.
newgame - Makes Connor play a new game. (Playing [...])
mybirthday [YYYY-MM-DD] - Saves your birthday.
nextbirthdays - Shows upcoming birthdays.
help - This message appears.
help hu - This message but in Hungarian.```""")

    @asyncio.coroutine
    async def helphu(self,channel):
        await self.client.send_message(channel, """```
Parancsok:
bestship - Connor véleménye a kedvenc RP párról.
newgame - Connor más játékot fog játszani. (Játszik [...] rész)
mybirthday [YYYY-MM-DD] - Elmenti a születésnapodat.
nextbirthdays - Mutatja a következő születésnapokat.
help - Ez az üzenet, de angolul.
help hu - Ezt az üzenetet megjeleníti.```""")
