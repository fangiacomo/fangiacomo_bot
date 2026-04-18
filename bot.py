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
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        print("Errore API:", e)
        return None


# 🔍 Controllo partite
def check_matches():
    try:
        data = get_live_matches()

        if not data:
            return

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


def get_live_matches():
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






import requests
import time
import os

# ======================
# CONFIG
# ======================

API_KEY = os.getenv("API_KEY")
API_HOST = os.getenv("API_HOST")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ======================
# TELEGRAM FUNCTION
# ======================

def send_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text
    }
    requests.post(url, data=payload)

# ======================
# LIVE MATCHES
# ======================

def get_live_matches():
    url = "https://v3.football.api-sports.io/fixtures?live=all"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)

        print("STATUS:", r.status_code)

        if r.status_code != 200:
            return []

        data = r.json()

        if "response" not in data:
            return []

        return data["response"]

    except Exception as e:
        print("ERRORE API:", e)
        return []

# ======================
# AI ANALYSIS (OPZIONALE)
# ======================

def ai_analysis(match_text):
    if not OPENAI_API_KEY:
        return "AI non attiva"

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": f"""
Analizza questa partita live:

{match_text}

Rispondi:
- score 0-10 probabilità gol
- WATCH o SKIP
"""
            }
        ],
        "temperature": 0.4
    }

    r = requests.post(url, headers=headers, json=data)

    try:
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "errore AI"

# ======================
# MAIN LOOP
# ======================

def run_bot():
    send_message("BOT LIVE ATTIVO")

    while True:
        matches = get_live_matches()

        for match in matches:

            try:
                home = match["teams"]["home"]["name"]
                away = match["teams"]["away"]["name"]

                hg = match["goals"]["home"]
                ag = match["goals"]["away"]

                minute = match["fixture"]["status"]["elapsed"]

                text = f"{home} vs {away} ({hg}-{ag}) min {minute}"

                analysis = ai_analysis(text)

                if "WATCH" in analysis or "8" in analysis or "9" in analysis:
                    send_message(f"🤖 AI ALERT:\n{text}\n\n{analysis}")

            except Exception as e:
                print("MATCH ERROR:", e)

        time.sleep(60)

# ======================
# START
# ======================

if __name__ == "__main__":
    run_bot()
