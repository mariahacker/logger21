import os
import json

try:
    import requests
except ImportError:
    print("Trying to Install required module: requests\n")
    os.system('python -m pip install requests')
    import requests

"""
CONSTANTS:
"""
URL = "https://raw.githubusercontent.com/mariahacker/logger21/main/main.py"

THIS_DIR = "/".join(os.getcwd().split("\\")[:-1])

with open("selfinfo.json") as f:
    ACTUAL_VERSION = float(json.load(f).get("VERSION"))

"""
UPDATER:
"""

def update(new_content:str, nw_version:str):
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(new_content)
    
    with open("selfinfo.json", "r+") as f:
        data = json.load(f)
        data["VERSION"] = nw_version
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

"""
RUN:
"""

if __name__ == "__main__":
    page = requests.get(URL)

    new_version = page.text.split("\n")[0].split(":")[-1]
    new_version = float(new_version)

    if new_version in range(100):

        if page.status_code != 200:
            print(f"error in connection, code {page.status_code}")
        elif new_version > ACTUAL_VERSION:
            update(page.text, str(new_version))
        elif new_version == ACTUAL_VERSION:
            print("nothing to update")
        elif new_version < ACTUAL_VERSION:
            print("wtf??")
    
    import main
    main.run()
