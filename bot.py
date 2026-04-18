import requests
import time
import os

# ======================
# ENV VARIABLES
# ======================

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ======================
# SAFE TELEGRAM
# ======================

def send_message(text):
    try:
        if not TELEGRAM_TOKEN or not CHAT_ID:
            print("MISSING TELEGRAM ENV VARIABLES")
            return

        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": text}, timeout=10)

    except Exception as e:
        print("TELEGRAM ERROR:", e)

# ======================
# SAFE LIVE MATCHES
# ======================

def get_live_matches():
    try:
        if not API_KEY or not API_HOST:
            return []

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
# SAFE PREMATCH
# ======================

def get_prematch():
    try:
        if not API_KEY or not API_HOST:
            return []

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
# SAFE PROBABILITY
# ======================

def calc_prob():
    return 0.70

# ======================
# MAIN BOT
# ======================

def run_bot():

    print("BOT STARTING...")

    # 🔥 NON CRASH START MESSAGE
    send_message("🔥 BOT LIVE ATTIVO")

    while True:
        try:
            print("LOOP RUNNING")

            live = get_live_matches()
            prematch = get_prematch()

            print("LIVE:", len(live))
            print("PREMATCH:", len(prematch))

            # ======================
            # LIVE ALERT
            # ======================
            if live:
                match = live[0]

                home = match["teams"]["home"]["name"]
                away = match["teams"]["away"]["name"]

                send_message(f"⚽ LIVE: {home} vs {away}")

            # ======================
            # PREMATCH SIMPLE
            # ======================
            for m in prematch[:3]:
                home = m["teams"]["home"]["name"]
                away = m["teams"]["away"]["name"]

                prob = calc_prob()

                if prob >= 0.70:
                    send_message(f"🔥 PREMATCH OVER 0.5\n{home} vs {away}\nProb: {prob}")

        except Exception as e:
            print("LOOP ERROR:", e)

        time.sleep(60)

# ======================
# START SAFE
# ======================

if __name__ == "__main__":
    run_bot()
