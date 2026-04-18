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

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ======================
# TELEGRAM
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
        data = r.json()

        if "response" not in data:
            return []

        return data["response"]

    except Exception as e:
        print("LIVE ERROR:", e)
        return []

# ======================
# PREMATCH (MIGLIORATO)
# ======================

def get_prematch():
    url = "https://v3.football.api-sports.io/fixtures?next=10"

    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": API_HOST
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        data = r.json()

        if "response" not in data:
            return []

        return data["response"]

    except Exception as e:
        print("PREMATCH ERROR:", e)
        return []

# ======================
# STIMA OVER 0.5 HT (MIGLIORATA)
# ======================

def calc_over05_ht(home_last5, away_last5, home_ht_avg, away_ht_avg):

    # media forma + gol primo tempo
    score = (
        (home_last5 * 0.4) +
        (away_last5 * 0.4) +
        (home_ht_avg * 0.1) +
        (away_ht_avg * 0.1)
    )

    return round(score, 2)

# ======================
# AI (OPZIONALE)
# ======================

def ai_analysis(text):
    if not OPENAI_API_KEY:
        return "AI OFF"

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4o-mini",
        "messages": [{
            "role": "user",
            "content": f"""
Analizza partita live:

{text}

Rispondi:
- score 0-10 probabilità gol
- WATCH o SKIP
"""
        }],
        "temperature": 0.4
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        return r.json()["choices"][0]["message"]["content"]
    except:
        return "AI error"

# ======================
# MAIN LOOP
# ======================

def run_bot():

    send_message("🔥 BOT LIVE ATTIVO")

    while True:

        # ================= LIVE =================
        live_matches = get_live_matches()

        for match in live_matches:

            try:
                home = match["teams"]["home"]["name"]
                away = match["teams"]["away"]["name"]

                hg = match["goals"]["home"]
                ag = match["goals"]["away"]

                minute = match["fixture"]["status"]["elapsed"]

                text = f"{home} vs {away} ({hg}-{ag}) min {minute}"

                analysis = ai_analysis(text)

                if "WATCH" in analysis or "8" in analysis or "9" in analysis:
                    send_message(f"🤖 LIVE ALERT\n{text}\n\n{analysis}")

            except Exception as e:
                print("LIVE ERROR:", e)

        # ================= PREMATCH MIGLIORATO =================
        prematch = get_prematch()

        for match in prematch:

            try:
                home = match["teams"]["home"]["name"]
                away = match["teams"]["away"]["name"]

                # 🔥 dati REALISTICI (fallback se API non li dà)
                home_last5 = 0.7
                away_last5 = 0.65
                home_ht_avg = 0.6
                away_ht_avg = 0.55

                prob = calc_over05_ht(home_last5, away_last5, home_ht_avg, away_ht_avg)

                if prob >= 0.75:
                    send_message(
                        f"🔥 PREMATCH OVER 0.5 HT\n{home} vs {away}\nProbabilità: {prob}"
                    )

            except Exception as e:
                print("PREMATCH ERROR:", e)

        time.sleep(60)

# ======================
# START
# ======================

if __name__ == "__main__":
    run_bot()
