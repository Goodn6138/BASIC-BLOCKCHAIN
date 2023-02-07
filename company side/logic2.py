from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import string
import random
import XcryptoX
import socket
import SQL_
import threading as thread
import json
import tempfile

#.......................................SOCKET CONNECTIONS................................
server = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
ip_addr = socket.gethostbyname(socket.gethostname())#input('ENTER IP ADDRESS: ', )
port =1234
server.bind((ip_addr , port))
server.listen()
print(ip_addr)
#.........................................SQL DATABASE.....................................
sql = SQL_.SQL()
PUBLIC_KEY_TB = "Reg_Companies"
BLOCK_TB = "Blocks"
COMPANY_DB = "Company.db"
try:
    sql.create_db(COMPANY_DB , PUBLIC_KEY_TB, "(company_name text ,public_key)")
except Exception as e:
    print(e)
#........................................LOGIC.............................................
SUCCESS = b'success'
FAILED = b'failed'

def recv(client,clients):
    try:
        data = client.recv(80000)
        print(data , "ppop")
        data = json.loads(data)
#........................................................REGISTRATION..................................
        if data['REQUEST'] == 'REGISTRATION':
            if "PUBLIC KEY" in data.keys() and "COMPANY NAME" in data.keys():
                public_key = data["PUBLIC KEY"]
                company_name = data["COMPANY NAME"]
                clients[company_name] = client
                try:
                    sql.insert_db("Company.db" ,PUBLIC_KEY_TB,"(?,?)", (company_name , public_key) )
                    print("DONE")
                    client.send(SUCCESS)
                except Exception as e:
                    print(e)
            else:
                client.send(FAILED)
#........................................................SEND TO......................................
                
        if data["REQUEST"] == 'SEND TO':
            if "COMPANY TO" in data.keys() and "COMPANY FROM" in data.keys() and "DATA" in data.keys():
                company_to = data['COMPANY TO']
                company_from = data["COMPANY FROM"]
                block_data = json.loads(data["DATA"])# , default = str)
             #   print(block_data)
                client.send(SUCCESS)
                
#........................................................CONFIRM COMPANY DIGITAL SIGNATURE FROM PUBLIC STORED PUBLIC KEY IF IT MATCHES SAVE IT ELSE DROP IT 
                public_key = sql.select_db(COMPANY_DB,'public_key', '{} WHERE company_name = ?'.format(PUBLIC_KEY_TB) ,company_from)
                #print("ojpfg")
                temp = ''.join(random.choices(string.ascii_letters + string.digits , k = 10))

                file = open(temp+'.pem', 'wb')
    
                pem_key = public_key[0][2:-1].encode()
                x = public_key[0][2:-1]
                x = x.replace('\\n', '\n')
                file.write(x.encode())
                file.close()
                
                crypt = XcryptoX.XcryptoX(data["PSWD"])
                block_sign = block_data.pop('digital signature')
                block_hash = block_data.pop('hash')
                block_nonce = block_data.pop('nonce')
      
                block_sign = block_sign.removeprefix("b'")
                block_sign = block_sign.removesuffix("'")
                block_sign = block_sign.encode().decode('unicode_escape').encode('raw_unicode_escape').decode('unicode_escape').encode('raw_unicode_escape')
      
                block_data['data'] = block_data['data'].removeprefix("b'")
                block_data['data'] = block_data['data'].removeprefix("'")
                block_data['data'] = block_data['data']#.encode()#.decode('unicode_escape').encode('raw_unicode_escape').decode('unicode_escape').encode('raw_unicode_escape')
        
                x = crypt.key_verify(block_sign,block_data['data'],temp+'.pem')
                if x == False:
                    client.send(SUCCESS)
                    data = b'save'+block_data
                    clients[company_to].send(data)
                    
                else:
                    client.send(SUCCESS)
            else:
                client.send(FAILED)

        else:       
            client.send(FAILED)
            print(data)
    except Exception as e:
        print(e , 'poop')
                
def send(client , msg):
    pass

clients = {}
def handle():
    while True:
        client, addr = server.accept()
        client.send(SUCCESS)

        recv_thread = thread.Thread(target = recv , args = (client,clients,))
        #send_thread = thread.Thread(target = send , args = (client,msg,))

        data = recv_thread.start()
        #send_thread.start()
        print(data)

handle()
