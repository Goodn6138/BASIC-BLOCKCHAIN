
#import pandas as pd
import XcryptoX
import json
path = r'C:\Users\user\Downloads\SOROJAPA 10 06 2022.xlsx'

class Load_sheet:
    def __init__(self ,path_to_excel_sheet , company_name , pswd):
        self.path_to_excel_sheet = path
        self.pswd = pswd
        self.company_name  = company_name
        self.crypt = XcryptoX.XcryptoX(pswd)
     
    def digest_excel(self, path_to_priv_key):
        file =open(self.path_to_excel_sheet , 'rb')
        data = file.read()
        df = {}
        df["data"] =data
        df["company"] = self.company_name
        df_json =json.dumps(df , default=str)

        df["digital signature"] = self.crypt.key_sign(df_json, path_to_priv_key) 
        df["hash"] =self.crypt.hash_function(json.dumps(df ,default =str))
        df["nonce"] = 0
        df_json = json.dumps(df,default=str)
        
        return df , df_json
    def confirm_signature(self,data , public_key_file):
        hash_ = data.pop('hash')
        nonce = data.pop('nonce')
        data_signature = data["digital signature"]
        sign = data.pop('digital signature')
        data_json = json.dumps(data , default=str)
        data["hash"] =  hash_
        data["digital signature"] = sign
        data['nonce'] = nonce
        return data , self.crypt.key_verify(data_signature, data_json, public_key_file)

priv_key = r'C:\Users\user\Desktop\GOODN\VIVIAN\company side\company app\private_key.pem'
pub_key = r'C:\Users\user\Desktop\GOODN\VIVIAN\company side\company app\pubic_key.pem'

#x = Load_sheet(path , "poopoo", 0 ,"poop")

#m,y = x.digest_excel(priv_key)
#y , t = x.confirm_signature(m , pub_key) 
#print(t)   
