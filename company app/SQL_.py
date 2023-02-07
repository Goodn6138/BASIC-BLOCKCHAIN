import sqlite3

class SQL:
    def __init__ (self):
        pass
    def create_db(self , database_name, table_name , param):
        conn = sqlite3.connect(database_name)
        cur = conn.cursor()
        cmnd = 'CREATE TABLE {} {}'.format(table_name , param)
        print(cmnd)
        t = '''{}'''.format(cmnd)
        print(t)
        conn.execute('''{}'''.format(cmnd))
        conn.commit()
        conn.close()

    def insert_db(self ,database_name, table_name ,variables, param):
        conn = sqlite3.connect(database_name)
        cmnd = 'INSERT INTO {} VALUES {}'.format(table_name, variables)
        conn.execute('''{}'''.format(cmnd), param)
        conn.commit()
        conn.close()
    
    def select_db(self, database_name , command , sql_trans):
        conn = sqlite3.connect(database_name)
        cmnd = 'SELECT {} FROM {}'.format(command , sql_trans)
        res = conn.execute('''{}'''.format(cmnd))
        return res.fetchall()
        

x = SQL()
#x.create_db("poopoo.db" ,"company", "(name text, key bytes)")
