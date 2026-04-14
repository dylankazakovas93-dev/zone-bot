from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN   = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id":    TELEGRAM_CHAT_ID,
        "text":       message,
        "parse_mode": "HTML"
    })

@app.route("/", methods=["GET"])
def health():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    print(f"Received: {data}")

    msg_type = data.get("type", "fill")
    action   = data.get("action", "").lower()
    price    = data.get("price", "?")
    zone     = data.get("zone", "?")

    if msg_type == "approach":
        send_telegram(f"🔔 <b>ZONE APPROACH</b>\nZone {zone}\nPrice within 10pts\nCheck chart now")

    elif action == "buy":
        sl = round(float(price) - 20, 2)
        tp = round(float(price) + 80, 2)
        send_telegram(f"✅ <b>LONG FILLED</b>\nZone {zone}\nEntry: {price}\nSL: {sl}\nTP: {tp}")

    elif action == "sell":
        sl = round(float(price) + 20, 2)
        tp = round(float(price) - 80, 2)
        send_telegram(f"✅ <b>SHORT FILLED</b>\nZone {zone}\nEntry: {price}\nSL: {sl}\nTP: {tp}")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
