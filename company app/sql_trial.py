import sqlite3

conn = sqlite3.connect('poo.db')

cur = conn.cursor()

#cur.execute(''' CREATE TABLE COMPANY
#                (COMPANY_NAME TEXT NOT NULL,
#                PUBLIC_KEY BYTES NOT NULL)''')
data = open(r'C:\Users\user\Desktop\GOODN\VIVIAN\company side\company app\pubic_key.pem' , 'rb')
data = data.read()

cur.execute('INSERT INTO COMPANY VALUES (? , ?)', ('poop' , data))
conn.commit()
#conn.execute('SELRCT * FROM COMPANY')

