
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import hashlib
class XcryptoX:
    def __init__(self , pswd):
        self.pswd = pswd #USER DEFINED PASSWORD USED TO ENCRYPT PRIVATE KEYS
    def hash_function(self , data):
        return hashlib.sha256(data.encode()).digest()
    def key_gen(self):
        '''
            PRIVATE KEY PUBLIC KEY GENERATION , USES USER DEFINED PASSWORD (pswd) TO GENERATE PRIVATE KEY AND PUBLIC KEY
            SAVES THE PEM FILES ON THE CWD AS public_key.pem AND private key.p
        '''
        pswd = self.pswd
        #GENERATE PRIVATE KEY PEM BYTES
        priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        pem_priv_key =  priv_key.private_bytes(
            encoding= serialization.Encoding.PEM,
            format = serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(pswd.encode())
        )
        #GENERATE PUBLIC KEY PEM BYTES
        pub_key = priv_key.public_key()
        pem_pb_key = pub_key.public_bytes(
            encoding = serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        #SAVE THE PEM BYTES
        file = open('public_key.pem' , 'wb')
        print(pem_pb_key)
        file.write(pem_pb_key)
        file.close()
        
        file = open('private_key.pem' , 'wb')
        file.write(pem_priv_key)
        file.close()
    #DIGITAL SIGNATURE
    
    def key_sign(self, data, priv_key_file):
        d_bytes = data.encode() #CONVERT DATA FROM STRING TO BYTES
        print(d_bytes)
        with open(priv_key_file,'rb') as key_file:
            priv_key =serialization.load_pem_private_key(key_file.read(), password=self.pswd.encode())
        key_file.close()
        digital_sign = priv_key.sign(d_bytes,
                                padding.PSS(
                                            mgf = padding.MGF1(hashes.SHA256()),
                                            salt_length=padding.PSS.MAX_LENGTH
                                            ),
                                hashes.SHA256())
        return digital_sign
    def key_verify(self,signature , data , public_key_file): #USE TO VERIFY STUFF
        b_data = data#.replace('\n' , '').encode()
        with open(public_key_file , 'rb') as key_file:
            x= key_file.read()
            pb_key = serialization.load_pem_public_key(x)
            try:
                pb_key.verify(
                    signature,
                    b_data,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH),
                    hashes.SHA256()
                    )
                return True
            except Exception as e:
                return False