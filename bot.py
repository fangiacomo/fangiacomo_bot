import requests
import time
import os

# 🔑 Variabili ambiente (Render)
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")


# 📩 Invio messaggi Telegram
def invia_messaggio(testo):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": testo})
    except Exception as e:
        print("Errore invio messaggio:", e)


# ⚽ Chiamata API live
def get_live_matches():
    try:
        url = "https://v3.football.api-sports.io/fixtures?live=all"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)

        print("STATUS CODE:", r.status_code)
        print("RAW RESPONSE:", r.text[:300])

        if r.status_code != 200:
            return []

        data = r.json()

        if "response" not in data:
            return []

        return data["response"]

    except Exception as e:
        print("ERRORE REQUEST:", e)
        return []

        for match in data.get("response", []):
            home = match.get("teams", {}).get("home", {}).get("name", "Home")
            away = match.get("teams", {}).get("away", {}).get("name", "Away")

            hg = match.get("goals", {}).get("home", 0)
            ag = match.get("goals", {}).get("away", 0)

            status = match.get("fixture", {}).get("status", {}).get("short", "")

            # 🔥 OVER 0.5 LIVE (almeno 1 gol)
            if status in ["1H", "2H"] and (hg + ag) >= 1:
                invia_messaggio(f"🔥 OVER 0.5 LIVE: {home} vs {away} ({hg}-{ag})")

            # ⚠️ 0-0 INTERVALLO
            if status == "HT" and (hg + ag) == 0:
                invia_messaggio(f"⚠️ 0-0 INTERVALLO: {home} vs {away}")

    except Exception as e:
        print("ERROR check_matches:", e)


# 🚀 MAIN LOOP
def main():
    invia_messaggio("✅ BOT LIVE PARTITE ATTIVO")

    while True:
        check_matches()
        time.sleep(60)


if __name__ == "__main__":
    main()
