mport requests
import os

print("BOT PARTITO")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("TOKEN:", TELEGRAM_TOKEN)
print("CHAT_ID:", CHAT_ID)

url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

try:
    r = requests.post(
        url,
        data={
            "chat_id": CHAT_ID,
            "text": "TEST BOT FUNZIONANTE"
        }
    )

    print("RESPONSE:", r.text)

except Exception as e:
    print("ERROR:", e)
