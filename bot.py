import requests
import os
import time

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

print("BOT STARTING TEST...")

def send_message():

    print("TOKEN:", TELEGRAM_TOKEN)
    print("CHAT_ID:", CHAT_ID)

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    try:
        r = requests.post(
            url,
            data={
                "chat_id": CHAT_ID,
                "text": "TEST MESSAGGIO BOT"
            },
            timeout=10
        )

        print("RESPONSE:", r.text)

    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":

    print("INVIO MESSAGGIO...")

    send_message()

    print("FINE TEST")

    while True:
        time.sleep(60)
