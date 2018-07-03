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

    def checkEntry(self,message):
        return message.content.startswith('new') or message.content.startswith('edit')
        
    def checkEdit(self,message):
        if message.content.startswith('abort'):
            return True
        self.cur.execute("SELECT ID FROM MEMBERS")
        query = self.cur.fetchall()
        query = [i[0] for i in query]
        if int(message.content) in query:
            return True
        else:
            return False

    def rowsToString(self, rows):
        return "\n".join(item[0] for item in rows)
            
    @asyncio.coroutine
    async def updateusers(self,message):
        members_curr = message.server.members
        members_curr = [str(i) for i in members_curr]
        self.cur.execute("SELECT username FROM MEMBERS")
        members_stored = self.cur.fetchall()
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
                    sql = """INSERT INTO MEMBERS(username)
                    VALUES(%s);"""
                    self.cur.execute(sql, [str(member)])
                    await self.client.send_message(message.channel, 'Sucessfully added:')
                    await self.client.send_message(message.channel, str(member))
                else:
                    await self.client.send_message(message.channel, 'These are your current members sir:')
                    self.cur.execute("SELECT * FROM MEMBERS")
                    rows = self.cur.fetchall()
                    await self.client.send_message(message.channel, '`'+self.rowsToString(rows)+'`')
                    await self.client.send_message(message.channel, 'Which username would you like to update? (type id number or abort)')
                    response = await self.client.wait_for_message(author=message.author,check=self.checkEdit)
                    if response.content.startswith('abort'):
                        await self.client.send_message(message.channel, 'Process aborted');
                        pass
                    else:
                        sql = """UPDATE MEMBERS SET username=%s 
                        WHERE ID=%s"""
                        self.cur.execute(sql,[str(member),int(response.content)])
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
        print (self.cur.fetchall()[0])
        await self.client.send_message(message.channel, '`'+self.rowsToString(self.cur.fetchall())+'`')
        
        
        