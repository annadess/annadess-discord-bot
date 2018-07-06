import discord
import asyncio
import os
import psycopg2
import random
import database
import datetime

class UserLogic:
    
    def __init__(self,client,dataobj):
        self.client = client
        self.dataobj = dataobj
        
    def checkEntry(self,message):
        return message.content.startswith('new') or message.content.startswith('edit')
        
    def checkEdit(self,message):
        if message.content.startswith('abort'):
            return True
        query = self.dataobj.selectFrom(["ID","MEMBERS"])
        query = [i[0] for i in query]
        if int(message.content) in query:
            return True
        else:
            return False
            
    def validate(self,date_text):
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
            return False
    
    @asyncio.coroutine
    async def updateusers(self,message):
        members_curr = message.server.members
        members_curr = [str(i) for i in members_curr]
        members_stored = self.dataobj.selectFrom(["username","MEMBERS"])
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
                    rows = self.dataobj.selectFrom(["*","MEMBERS"])
                    await self.client.send_message(message.channel, '```'+dataobj.rowsToString(rows)+'```')
                    await self.client.send_message(message.channel, 'Which username would you like to update? (type id number or abort)')
                    response = await self.client.wait_for_message(author=message.author,check=self.checkEdit)
                    if response.content.startswith('abort'):
                        await self.client.send_message(message.channel, 'Process aborted');
                        pass
                    else:
                        self.dataobj.updateSetWhere(['MEMBERS','username','ID',str(member),int(response.content)])
                        await self.client.send_message(message.channel, 'Entry successfully updated');
                        
        self.dataobj.conn.commit()
    
    @asyncio.coroutine
    async def mybirthday(self, message):
        author_id = self.dataobj.selectFromWhere(['ID','MEMBERS','USERNAME',str(message.author)])[0][0]
        if len(self.dataobj.selectFromWhere(['*','BIRTHDAYS','MEMBER_ID',author_id])) == 0 and self.validate(message.content[12:]):
            self.dataobj.insertInto(['BIRTHDAYS','birthdate , MEMBER_ID',message.content[12:],str(author_id)])
            self.dataobj.conn.commit()
        elif self.validate(message.content[12:]):
            self.dataobj.updateSetWhere(['BIRTHDAYS','birthdate','MEMBER_ID',message.content[12:],str(author_id)])
            self.dataobj.conn.commit()
            
    @asyncio.coroutine
    async def nextbirthdays(self, channel):
        birthdays = []
        for row in self.dataobj.selectFrom(['birthdate, MEMBER_ID', 'BIRTHDAYS']):
            birthdate, member_id = row
            username = self.dataobj.selectFromWhere(['username','MEMBERS','ID',member_id])[0][0]
            today = datetime.datetime.today().date()
            birthdate = birthdate.replace(year=today.year)
            if birthdate < today:
                birthdate.replace(year=today.year + 1)
            difference = today - birthdate
            birthdays.append((difference.dt.days,username))
        birthdays.sort()
        await self.client.send_message(channel, '```'+dataobj.rowsToString(birthdays)+'```')