import discord
import asyncio
import os
import psycopg2
import random

class Database:

    def establishConnection(self):
        self.conn = psycopg2.connect(os.environ.get('DATABASE_URL'), sslmode='require')
        self.cur = self.conn.cursor()

    def __init__(self,client):
        self.client = client
        self.establishConnection()

    def selectFrom(self, args):
        self.cur.execute("SELECT {0} FROM {1}".format(*args))
        return self.cur.fetchall()    
    
    def insertInto(self,args):
        sql = """INSERT INTO {0}({1})
                    VALUES(%s);""".format(*args[:2])
        self.cur.execute(sql, args[2:])
        
    def updateSetWhere(self,args):
        sql = """UPDATE {0} SET {1}=%s 
                        WHERE {2}=%s""".format(*args[:3])
        self.cur.execute(sql, args[3:])
        
    def checkEntry(self,message):
        return message.content.startswith('new') or message.content.startswith('edit')
        
    def checkEdit(self,message):
        if message.content.startswith('abort'):
            return True
        query = self.selectFrom(["ID","MEMBERS"])
        query = [i[0] for i in query]
        if int(message.content) in query:
            return True
        else:
            return False

    def rowsToString(self, rows):
        return "\n".join(str(item) for item in rows)
    
    @asyncio.coroutine
    async def updateusers(self,message):
        members_curr = message.server.members
        members_curr = [str(i) for i in members_curr]
        members_stored = self.selectFrom(["username","MEMBERS"])
        members_stored = [i[0] for i in members_stored]
        members_new = list(set(members_curr)-set(members_stored))
        if len(members_new)==0:
            await self.client.send_message(message.channel, 'Sir, my database is up to date with the members of this server, no changes required.')
        else:
            await self.client.send_message(message.channel, 'It seems there are new members sir.')
            for member in members_new:
                await self.client.send_message(message.channel, 'Would you like to add '+member+' as a new entry, or would you like to replace an entry?')
                await self.client.send_message(message.channel, '(type new or edit)')
                response = await self.client.wait_for_message(author=message.author,check=self.checkEntry)
                if response.content.startswith('new'):
                    self.insertInto(['MEMBERS','username',str(member)])
                    await self.client.send_message(message.channel, 'Sucessfully added:')
                    await self.client.send_message(message.channel, str(member))
                else:   
                    await self.client.send_message(message.channel, 'These are your current members sir:')
                    rows = self.selectFrom(["*","MEMBERS"])
                    await self.client.send_message(message.channel, '```'+self.rowsToString(rows)+'```')
                    await self.client.send_message(message.channel, 'Which username would you like to update? (type id number or abort)')
                    response = await self.client.wait_for_message(author=message.author,check=self.checkEdit)
                    if response.content.startswith('abort'):
                        await self.client.send_message(message.channel, 'Process aborted');
                        pass
                    else:
                        self.updateSetWhere(['MEMBERS','username','ID',str(member),int(response.content)])
                        await self.client.send_message(message.channel, 'Entry successfully updated');
                        
        self.conn.commit()

    @asyncio.coroutine
    async def closedb(self,channel):
        self.conn.close()
        await self.client.send_message(channel, 'Connection with database closed sir, ready for restart.');
        
    @asyncio.coroutine
    async def opendb(self,channel):
        self.conn.close()
        self.establishConnection()
        await self.client.send_message(channel, 'Connection with database reestablished sir.');
        
    @asyncio.coroutine
    async def runsql(self,message):
        self.cur.execute(message.content[7:])
        await self.client.send_message(message.channel, '```'+self.rowsToString(self.cur.fetchall())+'```')
        
        
        