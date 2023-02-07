import socket
from threading import Thread
import sqlite3

server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
ip_addr = socket.gethostbyname(socket.gethostname())
print(ip_addr)

server.bind((ip_addr , 1234))
server.listen()

request_ok = 'HTTP/1.1 200 OK\n\n'

docs =r'C:\Users\user\Desktop\GOODN\VIVIAN\server\webserver\docs'

def send(txt , client):
    print(txt)
    client ,addr = server.accept()
    data = txt.encode()
    client.send(data)
    #print('shosho')
    client.close()
        
def Recv(client):
#    while True:
#        client ,addr = server.accept()
        headers = client.recv(1024).decode()
        req = headers.split('\n')
        #client.close()

        try:
            try:
                instruction = req[0].split()[1]
            except Exception as e:
                instruction = ''
                print(e)
            print(instruction)    
            if instruction.startswit('/h?search='):
                serial_no = instruction.removeprefix('/?search=')
                conn = sqlite3.connect('blocks.db')
                cur = conn.cursor()
                cur.execute('SELECT * FROM blocks WHERE name=:name', {"name": serial_no})
                chain = cur.fetchall()
                print(chain)
                table = "<tr>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>"
                for i in chain:
                    table.format(i[0], i[1],i[2],i[3])
                file =open(docs+'\mining.html' , 'r')
                data = file.read()
                data = data.replace('**table**', table)

                data = request_ok + data
                send(data ,client)
              #  client.close()

                    
                            
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>CREATE TABLE , SEND TO USER WEBPAGE , return function
                
            if instruction.startswith('/action_page.php?'):
                miner = instruction.removeprefix('/action_page.php?')
                print(miner) #>>>>>>>>>>>>>>>>>>>>>>>VITU ZA MINING HAPA
            if instruction.startswith('/'):
                #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>SEND HOMEPAGE
                file = open(docs+'\index.html', 'r')
                data = file.read()
                data = request_ok + data
                send(data ,client)
                #client.close()
             #   print("poop")

        except Exception as e:
            print(e , "sdfsdfF")


def handle():
    client ,addr = server.accept()
    #req = client.recv(1024).decode()
        
    Recv(client)    
#    send(data , client)
#    thread_send = Thread(target = send, args = (data  ,client,))
#    thread_recv = Thread(target = recv , args = (client,))

 #   thread_send.start()
 #   thread_recv.start()
#    thread_send.start()
while True:
    client , addr = server.accept()
    Recv(client)

