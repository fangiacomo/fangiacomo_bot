import requests
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def invia_messaggio(testo):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": testo}
    requests.post(url, data=data)

partite = [
    {"match": "Team A vs Team B", "minute": 45, "home": 0, "away": 0, "halftime": True},
]

def check_partite():
    for p in partite:
        if p["halftime"] and p["home"] == 0 and p["away"] == 0:
            invia_messaggio(f"⚠️ 0-0 FINE PRIMO TEMPO: {p['match']}")

def main():
    if TOKEN and CHAT_ID:
        invia_messaggio("✅ Bot live 0-0 attivo")

    while True:
        check_partite()
        time.sleep(60)

if __name__ == "__main__":
    main()
