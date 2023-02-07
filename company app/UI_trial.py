
import EXCEL_2 #USED TO PREPARE EXCEL SHEETS TO APPROPRIATE FORMAT
import json     #CREATING JSON STRINGS
from tkinter import *   #CREATING UI
import XcryptoX #FOR ENCRYPTION
import Network  #FOR NETWORKING
import os 
#..........................................................REGISTRATION BLOCK............................................
class REG:
    def __init__(self , root):
#.........................................................INITIALING THE USER INTERFACE..................................
        root.geometry('380x400')
        root.configure(bg = 'black')
        self.BG_COLOR = 'black'
        self.FG_COLOR = 'white'
        self.FONT = 'Helvetica 10 bold'

        self.l1 = Label(root , text = "WELCOME TO BLOCK APP" , fg = self.FG_COLOR, bg = self.BG_COLOR , font = "Helvetica 12 bold")
        self.l1.place(x = 80 , y = 10)

        self.l2 = Label(root , text = "FILL IN THE DETAILS TO REGISTER" , fg = self.FG_COLOR, bg = self.BG_COLOR , font = "Helvetica 12 bold")
        self.l2.place(x = 50 , y = 50)

        self.l3 = Label(root , text = "SERVER IP:" , fg = self.FG_COLOR, bg = self.BG_COLOR , font = "Helvetica 12 bold")
        self.l3.place(x = 10 , y = 90)

        self.IP = Entry(root , width = 30, font = self.FONT)
        self.IP.place(x = 160 , y = 90)

        self.l4 = Label(root , text = "COMPANY_NAME: " , fg = self.FG_COLOR, bg = self.BG_COLOR , font = "Helvetica 12 bold")
        self.l4.place(x = 10 , y = 130)

        self.COMPANY = Entry(root , width = 30, font = self.FONT)
        self.COMPANY.place(x = 160 , y = 130)

        self.l5 = Label(root , text = "PASSWORD: " , fg = self.FG_COLOR, bg = self.BG_COLOR , font = "Helvetica 12 bold")
        self.l5.place(x = 10 , y = 170)

        self.PASS = Entry(root , width = 30, font = self.FONT)
        self.PASS.place(x = 160 , y = 170)

        self.REG_BTN = Button(root , text = "REGISTER",font = self.FONT,bg = "red",command = self.Reg)
        self.REG_BTN.place(x = 10, y =210)
    #GET IP_ADDRESS ,PASS,COMPANY NAME ,GENERATE PRIVATE PUBLIC KEY FROM PASSWORD,
    # CONNECT TO IP ADDRESS,SEND COMPANY NAME AND PUBLIC KEY TO SERVER

    def Reg(self):
        company_name = self.COMPANY.get() #company_name
        ip_address = self.IP.get() #server ip address
        password = self.PASS.get() #password

        crypt = XcryptoX.XcryptoX(password)
        crypt.key_gen()
        key = open(r'public_key.pem' , 'rb')
        public_key = key.read()
        print(public_key)

        data = {'REQUEST': 'REGISTRATION',  #DATA TO BE SENT
                "PUBLIC KEY":public_key,
                "COMPANY NAME":company_name,
                }
        data_json = json.dumps(data , default=str) #JSON FORMAT OF THE DATA
        connection = Network.Connection(ip_address , 1234) #CONNNECTING TO THE SERVER
        if connection.recv(1024) != 'success':
            print('FAILED')
        else:
            connection.send(data_json)
            if connection.recv(1024) != "success":
                print('FAILED')
            else:                
                print('CONTENT SAVED')


#............................................................RUNNING APP BLOCK..................................
class APP:
    def __init__(self,root):
        root.geometry('600x400')
        root.configure(bg = 'black')

        self.BG_COLOR = 'black'
        self.FG_COLOR = 'white'
        self.FONT = 'Helvetica 12 bold'

        self.l1= Label(root, text = 'SERVER_IP:', fg= self.FG_COLOR , bg = self.BG_COLOR  , font = self.FONT)
        self.l1.place(x = 10 , y = 40)

        self.l4 = Label(root , text = 'PASSWORD' , fg= self.FG_COLOR , bg = self.BG_COLOR  , font = self.FONT)
        self.l4.place(x = 10 ,y = 120)

        self.l5 = Label(root, text = 'COMPANY',fg= self.FG_COLOR , bg = self.BG_COLOR  , font = self.FONT)
        self.l5.place(x = 10 , y = 200)
        
        self.IP = Entry(root , width = 30, font = self.FONT)
        self.IP.place(x = 10 , y = 80)
        
        self.l2= Label(root, text = 'DOCUMENT:', fg= self.FG_COLOR , bg = self.BG_COLOR  , font = self.FONT)
        self.l2.place(x = 320 , y = 120)

        self.PSWD = Entry(root, width = 30, font = self.FONT)
        self.PSWD.place(x = 10 , y = 160)

        self.COMPANY = Entry(root, width = 30, font = self.FONT)
        self.COMPANY.place(x = 10, y = 240)
        self.DOCS = Entry(root , width = 30, font = self.FONT)
        self.DOCS.place(x = 320 , y = 160)

        self.l3= Label(root, text = 'SEND TO:', fg= self.FG_COLOR , bg = self.BG_COLOR  , font = self.FONT)
        self.l3.place(x = 320 , y = 200)

        self.COMPANY_TO = Entry(root , width = 30, font = self.FONT)
        self.COMPANY_TO.place(x = 320 , y = 240)

        self.SEND_BTN = Button(root , text  = "SEND", font = self.FONT , bg = 'red',command = self.SEND)
        self.SEND_BTN.place(x=320 , y = 300)
        


    def init(self,connection , company_name):
        data = {"REQUEST": 'NAME',
                "NAME": company_name,
                }
        connection.send(json.dumps(data, default=str))
        return connection.recv(1024)            
        
    def SEND(self):
        #TAKING IP ADDRESS , DOCUMENT PATH , COMPANY RECIPIENT
        ip_address = self.IP.get()
        document = self.DOCS.get()
        company_rcvr = self.COMPANY_TO.get()
        company_name = self.COMPANY.get()
        password = self.PSWD.get()
        
        connection  = Network.Connection(ip_address , 1234)     
        command =  connection.recv(1024)
        if  command == 'success':
            sheet = EXCEL_2.Load_sheet(document , company_name,password)
            excel , excel_json = sheet.digest_excel('private_key.pem')

            data  = {"REQUEST": 'SEND TO',
                    "COMPANY TO": company_rcvr, 
                    "COMPANY FROM":company_name,
                    "DATA": excel_json,
                     "PSWD":password
                    }
            print(len(json.dumps(data, default=str)))
            
            connection.send(json.dumps(data, default=str))    
        if command.startswith(b'save'):
                file = open('temp.xlsx' , 'wb')
                data = command.removeprefix(b'save')
                file.write(data)
                file.close()
                

        else:
            print(command)


# C:\Users\user\Downloads\SOROJAPA 10 06 2022.xlsx'
root = Tk()

files = os.listdir()
if 'private_key.pem' in files or 'public_key.pem' in files: #CHECK IF ITS FAST TIME REGISTERING
    APP(root)
else:
    REG(root)


root.mainloop()
    
 
