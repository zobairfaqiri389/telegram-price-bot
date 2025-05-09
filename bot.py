import os
from flask import Flask, request
import telebot

API_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# ست کردن Webhook
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

# هندل کردن پیام‌های دریافتی از تلگرام
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "سلام زبیر! رباتت فعاله.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# روت اصلی که تلگرام بهش POST می‌فرسته
@app.route("/", methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content type', 403

# اجرا در پورت رندر
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
