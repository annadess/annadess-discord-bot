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
        
    def selectFromWhere(self, args):
        sql = "SELECT {0} FROM {1} WHERE {2}=%s".format(*args[:3])
        self.cur.execute(sql,args[3:])
        return self.cur.fetchall() 
    
    def insertInto(self,args):
        sql = """INSERT INTO {0}({1})
                    VALUES(%s"""+(", %s")*len(args[3:])+");"
        sql = sql.format(*args[:2])
        self.cur.execute(sql, args[2:])
        
    def updateSetWhere(self,args):
        sql = """UPDATE {0} SET {1}=%s 
                        WHERE {2}=%s""".format(*args[:3])
        self.cur.execute(sql, args[3:])

    def rowsToString(self, rows):
        return "\n".join(str(item) for item in rows)
        
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
        
        
        