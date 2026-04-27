from flask import Flask, request
import requests
import json

app = Flask(__name__)

# Настройки Telegram
TELEGRAM_TOKEN = "8635674583:AAGstQqoxW4u6vl_XSJLgbkB2zsgY953O_0"
CHAT_ID = "793481696"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data:
        # Извлекаем информацию из алерта Grafana
        title = data.get('title', 'Grafana Alert')
        message = data.get('message', 'No message')
        state = data.get('state', 'unknown')
        
        # Формируем красивое сообщение
        text = f"🚨 <b>{title}</b>\n\n{message}\n\nState: <code>{state}</code>"
        send_telegram_message(text)
        return 'OK', 200
    return 'Bad Request', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)