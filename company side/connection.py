import socket

class Serve:
    def __init__(self):
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.port = 1234
        self.server = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        print("SERVING AT http://{}:{}".format(self.ip_address,self.port))
        self.server.bind((self.ip_address, self.port))   
      #  self.client = []

    def init_server(self):
        self.server.listen()
        client , addr = self.server.accept()
        self.client = client

    def recv(self , bytes = 2024):
        print(self.client)
        return self.client.recv(bytes)
    
    def send(self, message):
        self.client.send(message.encode())