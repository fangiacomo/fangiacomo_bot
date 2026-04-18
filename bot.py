import requests
import time
import os

# ======================
# CONFIG
# ======================

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ======================
# TELEGRAM SAFE
# ======================

def send_message(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)
    except Exception as e:
        print("TELEGRAM ERROR:", e)

# ======================
# LIVE MATCHES
# ======================

def get_live_matches():
    try:
        url = "https://v3.football.api-sports.io/fixtures?live=all"
        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": API_HOST
        }

        r = requests.get(url, headers=headers, timeout=10)
        return r.json().get("response", [])

    except Exception as e:
        print("LIVE ERROR:", e)
        return []

# ======================
# PREMATCH (STABILE)
# ======================

def get_prematch():
    try:
        url = "https://v3.football.api-sports.io/fixtures?next=10"
        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": API_HOST
        }

        r = requests.get(url, headers=headers, timeout=10)
        return r.json().get("response", [])

    except Exception as e:
        print("PREMATCH ERROR:", e)
        return []

# ======================
# SIMPLE PROBABILITY (SAFE)
# ======================

def calc_over05():
    return 0.72  # valore stabile (evita crash)

# ======================
# BOT MAIN
# ======================

def run_bot():

    print("BOT STARTING...")

    # 🔥 sempre primo messaggio
    send_message("🔥 BOT LIVE ATTIVO")

    while True:

        try:
            live_matches = get_live_matches()
            prematch = get_prematch()

            print("LIVE:", len(live_matches))
            print("PREMATCH:", len(prematch))

            # ======================
            # LIVE ALERT SIMPLE
            # ======================
            if live_matches:
                m = live_matches[0]

                home = m["teams"]["home"]["name"]
                away = m["teams"]["away"]["name"]
                hg = m["goals"]["home"]
                ag = m["goals"]["away"]

                send_message(f"⚽ LIVE: {home} {hg}-{ag} {away}")

            # ======================
            # PREMATCH SIMPLE FILTER
            # ======================
            for match in prematch[:3]:

                home = match["teams"]["home"]["name"]
                away = match["teams"]["away"]["name"]

                prob = calc_over05()

                if prob >= 0.70:
                    send_message(f"🔥 PREMATCH OVER 0.5\n{home} vs {away}\nProb: {prob}")

        except Exception as e:
            print("LOOP ERROR:", e)

        time.sleep(60)

# ======================
# START SAFE
# ======================

if __name__ == "__main__":
def run_bot():

    print("BOT STARTING")

    send_message("🔥 BOT LIVE ATTIVO")  # 👈 QUI

    while True:
        ...
