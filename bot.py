import discord
import asyncio
import os
import psycopg2

client = discord.Client()
prefix = '.'
conn = psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode='require')
cur = conn.cursor()

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
    elif isCommand(message, 'updateusers'):
        sql = """INSERT INTO MEMBERS(username)
             VALUES(%s);"""
        members_curr = message.server.members
        cur.execute("SELECT username FROM MEMBERS")
        members_stored = cur.fetchall()
        members_new = list(set(members_curr)-set(members_stored))
        cur.executemany(sql, [str(i) for i in members_new])
        conn.commit()
        await client.send_message(message.channel, 'Sucessfully added:')
        await client.send_message(message.channel, members_new)
    elif isCommand(message, 'closedb'):
        conn.close()

client.run(os.environ.get('BOT_TOKEN'))
