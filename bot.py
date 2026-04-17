import requests
import time
import os

TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")

def invia_messaggio(testo):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": testo})

def get_live_matches():
    url = "https://v3.football.api-sports.io/fixtures?live=all"
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }
    return requests.get(url, headers=headers).json()

def check_matches():
    data = get_live_matches()

    for match in data.get("response", []):
        home = match["teams"]["home"]["name"]
        away = match["teams"]["away"]["name"]

        hg = match["goals"]["home"]
        ag = match["goals"]["away"]

        status = match["fixture"]["status"]["short"]

        if status == "HT" and hg == 0 and ag == 0:
            invia_messaggio(f"⚠️ 0-0 INTERVALLO: {home} vs {away}")

def main():
    invia_messaggio("✅ Bot live partite reali attivo")

    while True:
        try:
            check_matches()
        except:
            pass
        time.sleep(60)

if __name__ == "__main__":
    main()
