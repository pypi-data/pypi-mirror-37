import sqlite3 as sq
import os
from difflib import get_close_matches
from datetime import datetime
memory = ":memory:"
class connect(object):
    def __init__(self,adds=memory,logs=True):
        self.adds = adds
        self.conn = sq.connect(adds) if adds==memory else sq.connect("."+adds+".sunlite")
        self.cur = self.conn.cursor()
        self.latest = ''
        self.logs = logs
        if self.conn:
            if logs:
                print("Sunlite connected to : "+adds)
            self.cur.execute('''CREATE TABLE IF NOT EXISTS "headers" (
	                "last"	TEXT,
	                "date"	BLOB,
                    "time"  BLOB,
	                "name"	TEXT NOT NULL,
	                "identity"	INTEGER NOT NULL DEFAULT 0 PRIMARY KEY AUTOINCREMENT,
	                "password"	BLOB NOT NULL DEFAULT 'pass'
                        );''')
            self.conn.commit()
        else:
            if logs:
                print("Sunlite can't connect.")
            exit
    
    def new(self,args,password='pass'):
        '''
        creates new header
        '''
        def header(self,name,password):
            try:
                self.cur.execute('''
                SELECT name FROM headers where name=='{0}'
                '''.format(name))
                if self.cur.fetchone()[0] == name:
                    print("Error : Header {0} already Exists".format(name))
                    return
                    
            except:
                if password=='pass':
                    print("Warning : No password specified")
                    pass
                date = str(datetime.now().date())
                time = str(datetime.now().time())
                self.cur.execute('''
                INSERT INTO HEADERS(name,date,password,time) VALUES('{0}','{1}','{2}','{3}')
                '''.format(name,date,password,time))
                self.conn.commit()
                self.cur.execute('''
                CREATE TABLE "{0}" (
	            "identity"	INTEGER NOT NULL DEFAULT 1 PRIMARY KEY AUTOINCREMENT UNIQUE,
	            "datas"	BLOB NOT NULL DEFAULT 'no data',
                "name" TEXT 
                );'''.format(name))
                with open('config','w') as f:
                    f.write(name)
                    f.close()
                self.conn.commit()
                if self.logs:
                    print("new column added "+self.latest)
                return
        
        header(self,args,password)
    
    def List(self):
        tbnames = []
        values = {}
        self.cur.execute('''
        SELECT name,identity from headers
        ''')
        for i in list(self.cur.fetchall()):
            tbnames += [list(i)]
        for i in tbnames:
            self.cur.execute('''
            SELECT name,datas from {0}
            '''.format(i[0]))
            p = {}
            for u in self.cur.fetchall():
                a = list(u)
                p[a[0]] = a[1]
            values[i[0]] = p
        return values

    def push(self,name,datas,target='l'):
            with open('config','r') as f:
                latest = f.read()
                f.close()
            target = latest if target=='l' else target
            self.cur.execute('''INSERT INTO {0}(name,datas) VALUES('{1}','{2}') '''.format(target,name,datas))
            self.conn.commit()
            if self.logs:
                print("Success : Pushed {0} to {1}".format(name,target))
            return True
    def headers(self):
        ''''
        Returns the names of headers in database
        '''
        tbnames = []
        self.cur.execute('''
        SELECT name,identity from headers
        ''')
        for i in list(self.cur.fetchall()):
            tbnames += [list(i)]
        return tbnames
    def pull(self,name):
        '''Pulls a data from database'''
        try:
            a = self.List()
            keyprofile = {}
            if name in a:
                return a[name]
            for i in list(a.keys()):
                for b in list(a[i].keys()):
                    value = a[i][b]
                    keyprofile[b] = value
            return keyprofile[name]
        except:
            print("Error: Unable to find data")

    def get(self,header):
        '''gets a header as it is'''
        self.cur.execute('''
            SELECT name,datas from {0}
            '''.format(header))
        return self.cur.fetchall()
    def beauty(self):
        '''Beauty prints a database'''
        for i in self.List():
            print(" :" +i)
            for j in self.List()[i]:
                print("   "+j+"\t "+self.pull(j))
    

        


