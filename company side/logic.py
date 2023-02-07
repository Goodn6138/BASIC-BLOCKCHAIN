#import connection
import socket
import threading as thread
import json
import SQL_

sql = SQL_.SQL()
#sql.create_db("Companies.db", "Reg_companies" , "(company_name,public key)")
#con = connection.Serve()
SUCCESS= b"success"
FAILED = b"failed"
#con.init_server()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostbyname(socket.gethostname()),1234))
server.listen()
while True:
    client,addr = server.accept()
    
    client.send(SUCCESS)
    data = client.recv(10000)#.decode()
    
    #print(len(data))
    try:
        print('tookiku')
        print(len(data))
        data = json.loads(data)
      #  print(data)
        if data["REQUEST"] == 'REGISTRATION': #REGISTRATION THINGIS
            
            if "PUBLIC KEY" in data.keys() and "COMPANY NAME" in data.keys():
                public_key = data["PUBLIC KEY"]
                company_name = data["COMPANY NAME"]
             
                try:
                    
                    sql.insert_db("Companies.db" ,"Reg_companies","(?,?)", (company_name , public_key) )
                    print("DONE")
                    client.send(SUCCESS)
                except Exception as e:
                    print(e,'ioffg')

            else:
                client.send(FAILED)

            #RECIEVE PUBLIC KEYS
            #RECIEVE COMPANY NAMES
            #SAVE COMPANY NAME & PUBLIC KEYS IN COMPANY DATABASE
        
        if data["REQUEST"] == 'SEND TO':#SEND THINGI
            if "COMPANY TO" in data.keys() and "COMPANY FROM" in data.keys() and "DATA" in data.keys():
                print(data['COMPANY TO'])
            
                #.............................SAVE DETAILS THEN SEND IT TO COMPANY_NAME
            else:
                client.send(FAILED)
                
        if data["REQUEST"] =='GET':#GET THINGIS
            if "BLOCK HASH" in data.keys():
                block_hash = data["BLOCK HASH"]
            else:
                client.send(FAILED)
            #RECIECVE COMPANY NAME
            #RECIEVE COMPANY DATA
            #SEND COMPANY DATA
            pass
        
        if data["REQUEST"] =='POST':#POST THINGIS

            #RECIEVE COMPANY DATA
            #VERIFY DIGITAL SIGNATURE
            #IF TRUE:
                #ADD TO DATABASE
            #ELSE:
            #   CANCEL
            pass
        else:
            client.send('REQUEST {} FAILED'.format(data["REQUEST"]))
    except Exception as e:
        print (e, 'poop')

