import sqlite3

class SQL:
    def __init__ (self):
        pass
    def create_db(self , database_name, table_name , param):
        '''
            database_name = name of your database
            table_name = name of your table
            param = parameters placed into the database

        '''
        conn = sqlite3.connect(database_name)
        cur = conn.cursor()
        cmnd = 'CREATE TABLE {} {}'.format(table_name , param)
        print(cmnd)
        t = '''{}'''.format(cmnd)
        print(t)
        
        cur.execute('''{}'''.format(cmnd))
        conn.commit()
        conn.close()

    def insert_db(self ,database_name, table_name ,variables, param):
        '''
            database_name = name of your database
            table_name = name of your table
            param = parameters placed into the database
            variables = variables placed into the database e.g (?, ?)

        '''
        conn = sqlite3.connect(database_name)
        cur = conn.cursor()
        cmnd = 'INSERT INTO {} VALUES {}'.format(table_name, variables)
        cur.execute('''{}'''.format(cmnd), param)
        conn.commit()
        conn.close()
    
    def select_db(self, database_name , command , sql_trans ,value):
        '''
            database_name = name of your database
            command = command to be executed e.g * or coloumns
            sql_trans = transactionsal info from the database
            value
        ''' 
        conn = sqlite3.connect(database_name)
        cur = conn.cursor()
        cmnd = 'SELECT {} FROM {}'.format(command , sql_trans)
        res = cur.execute('{}'.format(cmnd) , (value,))
        return res.fetchone()
        

#x = SQL()
#x.create_db("poopoo.db" ,"company", "(name text, key bytes)")
