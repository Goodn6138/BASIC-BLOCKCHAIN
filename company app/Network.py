import socket

class Connection:
    def __init__(self , ip_addr , port):
        self.ip_addr = ip_addr
        self.port = port
        self.client = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)
        self.client.connect((self.ip_addr ,self.port))
    
    def send(self , message):
            self.client.send(message.encode())
    
    def recv(self, bytes = 1024):
            return self.client.recv(1024).decode()
        
#x= Connection(socket.gethostbyname(socket.gethostname()) ,1235)
