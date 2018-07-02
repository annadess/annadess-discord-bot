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
    
def checkEntry(message):
    return message.content.startswith('new') or message.content.startswith('edit')
    
def checkEdit(message):
    if message.content.startswith('abort'):
        return True
    cur.execute("SELECT ID FROM MEMBERS")
    query = cur.fetchall()
    query = [i[0] for i in query]
    print(query)
    if int(message.content) in query:
        return True
    else:
        return False
        
@asyncio.coroutine
@client.event
async def on_message(message):
    if isCommand(message,'bestship'):
        await client.send_message(message.channel, 'Sir, the Kuno and Wyn pairing, is undoubtedly, the best pairing in this currently running role playing game.')
    elif isCommand(message, 'updateusers'):
        members_curr = message.server.members
        cur.execute("SELECT username FROM MEMBERS")
        members_stored = cur.fetchall()
        members_new = list(set(members_curr)-set(members_stored))
        print(members_new)
        print(len(members_new))
        if len(members_new)==0:
            await client.send_message(message.channel, 'Sir, my database is up to date with the members of this server, no changes required.')
        else:
            await client.send_message(message.channel, 'It seems there are new members sir.')
            for member in members_new:
                await client.send_message(message.channel, 'Would you like to add '+member.name+' as a new entry, or would you like to replace an entry?')
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
                        WHERE ID=%d"""
                        cur.execute(sql,str(member),int(response.content))
                        await client.send_message(message.channel, 'Entry successfully updated');
                        
        conn.commit()
    elif isCommand(message, 'closedb'):
        conn.close()
        await client.send_message(message.channel, 'Connection with database closed sir, ready for restart.');
        
client.run(os.environ.get('BOT_TOKEN'))
