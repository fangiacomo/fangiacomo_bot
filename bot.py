import requests
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def invia_messaggio(testo):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": testo}
    requests.post(url, data=data)

invia_messaggio("✅ Bot attivo")

while True:
    time.sleep(60)
