import discord
import asyncio
import os
import psycopg2
import random
import bot

client = bot.client
conn = psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode='require')
cur = conn.cursor()

def establishConnection():
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode='require')
    cur = conn.cursor()

def checkEntry(message):
    return message.content.startswith('new') or message.content.startswith('edit')
    
def checkEdit(message):
    if message.content.startswith('abort'):
        return True
    cur.execute("SELECT ID FROM MEMBERS")
    query = cur.fetchall()
    query = [i[0] for i in query]
    if int(message.content) in query:
        return True
    else:
        return False

@asyncio.coroutine
async def updateusers(message):
    members_curr = message.server.members
    members_curr = [str(i) for i in members_curr]
    cur.execute("SELECT username FROM MEMBERS")
    members_stored = cur.fetchall()
    members_stored = [i[0] for i in members_stored]
    members_new = list(set(members_curr)-set(members_stored))
    if len(members_new)==0:
        await client.send_message(message.channel, 'Sir, my database is up to date with the members of this server, no changes required.')
    else:
        await client.send_message(message.channel, 'It seems there are new members sir.')
        for member in members_new:
            await client.send_message(message.channel, 'Would you like to add '+member+' as a new entry, or would you like to replace an entry?')
            await client.send_message(message.channel, '(type new or edit)')
            response = await client.wait_for_message(author=message.author,check=checkEntry)
            if response.content.startswith('new'):
                sql = """INSERT INTO MEMBERS(username)
                VALUES(%s);"""
                cur.execute(sql, [str(member)])
                await client.send_message(message.channel, 'Sucessfully added:')
                await client.send_message(message.channel, str(member))
            else:
                await client.send_message(message.channel, 'These are your current members sir:')
                cur.execute("SELECT * FROM MEMBERS")
                rows = cur.fetchall()
                for r in rows:
                    await client.send_message(message.channel, '`'+str(r)+'`');
                await client.send_message(message.channel, 'Which username would you like to update? (type id number or abort)')
                response = await client.wait_for_message(author=message.author,check=checkEdit)
                if response.content.startswith('abort'):
                    await client.send_message(message.channel, 'Process aborted');
                    pass
                else:
                    sql = """UPDATE MEMBERS SET username=%s 
                    WHERE ID=%s"""
                    cur.execute(sql,[str(member),int(response.content)])
                    await client.send_message(message.channel, 'Entry successfully updated');
                    
    conn.commit()

@asyncio.coroutine
async def closedb(channel):
    conn.close()
    await client.send_message(channel, 'Connection with database closed sir, ready for restart.');
    
@asyncio.coroutine
async def opendb(channel):
    conn.close()
    establishConnection()
    await client.send_message(channel, 'Connection with database reestablished sir.');
    
    
    