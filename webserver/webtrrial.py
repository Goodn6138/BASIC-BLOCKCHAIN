from threading import Thread
import socket
import sqlite3

doc = r'C:\Users\user\Desktop\GOODN\VIVIAN\server\webserver\docs'
request_ok = 'HTTP/1.1 200 OK\n\n'
db = r"C:\Users\user\Desktop\VIVIAN\server\company side\BLOCK_CHAIN.db"

#>>>>>>>>>>>>>>>>>>>>>>SERVER SET UP>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>#
server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
ip = socket.gethostbyname(socket.gethostname())
print(ip)
port = 80
server.bind((ip , port))
server.listen()

def handle(client):
        req = client.recv(1024).decode()
        headers = req.split('\n')
        print(req)
        if headers[0].split() == ' ':
                instruction = '/' #default to homepage
                file = open(doc+'/index.html' , 'r')
                page = file.read()
                page = request_ok + page
                client.send(page.encode())
                client.close()
                return
        else:
                try:
                        instruction = headers[0].split()[1]
                        if instruction.startswith('/?search='): #SEARCHING database page
                                serial_no = instruction.removeprefix('/?search=')
                                conn = sqlite3.Connection(db)
                                cur = conn.cursor()
                                try:
                                        serial_no = int(serial_no)
                                except Exception as e:
                                        serail_no = serial_no
                                print(type(serial_no))
                                cur.execute("SELECT * FROM chain WHERE serial_number =:name", {"name": serial_no})
                                chain = cur.fetchall()
                                conn.commit()
                                conn.close()
                                
                                table = "\n<tr>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n<td>{}</td>\n</tr>"
                                table_fmt = table
                                print(chain)
                                x = ''
                                
                                if chain != []: #if the serial number doesnt exist
                                        for i in chain:
                                                table = f"<tr>\n<td>{i[0]}</td>\n<td>{i[2]}</td>\n<td>{i[3]}</td>\n<td>{i[4]}</td>\n<td>{i[5]}</td>/n<td>{i[6]}</td>/n/n<td>{i[7]}</td>/n<td>{i[8]}</td>/n<td>{i[9]}</td>/n<td>{i[10]}</td></tr>"
                                                x = x+table
                                        table = x
                                        file = open(doc+'\mining.html' , 'r')
                                        page = file.read()
                                        page = page.replace('**table**' , table)
                                        page = request_ok + page
                                        client.send(page.encode())
                                        client.close()
                                        return
                                else:
                                        table = f"\n<tr>\n<td>NULL</td>\n<td>NULL</td>\n<td>NULL</td>\n<td>NULL</td>\n</tr>"
                                        file = open(doc+'\mining.html' , 'r')
                                        page = file.read()
                                        page = page.replace('**table**' , table)
                                        page = request_ok + page
                                        client.send(page.encode())
                                        client.close()
                                        return
                        if instruction.startswith('/action_page.php?'): #MINING PAGE
                                file = open(r'C:\Users\user\Desktop\GOODN\VIVIAN\miners side\templates\mine.html' , 'r')
                                page = file.read()
                                page = request_ok+page
                                client.send(page.encode())
                                client.close()
                                return
                        if instruction.startswith('/'):#INDEX PAGE
                                file = open(doc + '\index.html' , 'r')
                                page = file.read()
                                page = request_ok + page
                                client.send(page.encode())
                                client.close()
                                return

                except Exception as e:
                        print(e)
while True:                     
        client , addr = server.accept()
        handle(client)
