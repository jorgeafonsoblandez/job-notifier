import os
import requests

token = os.environ.get("TELEGRAM_BOT_TOKEN")
chat_id = os.environ.get("TELEGRAM_CHAT_ID")

print(f"Token present: {bool(token)}")
print(f"Chat ID present: {bool(chat_id)}")

url = f"https://api.telegram.org/bot{token}/sendMessage"
payload = {
    "chat_id": chat_id,
    "text": "🛠️ Test message from job aggregator debug script"
}

resp = requests.post(url, json=payload)
print("Status Code:", resp.status_code)
print("Response Body:", resp.text)