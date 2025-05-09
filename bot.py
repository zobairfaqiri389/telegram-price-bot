import os
import telebot
from flask import Flask, request

# دریافت توکن و آدرس وبهوک از متغیرهای محیطی
BOT_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# حذف وبهوک قبلی و تنظیم وبهوک جدید
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

# پاسخ به دستور /start
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "سلام زبیر! رباتت فعاله. لطفاً عکس یا پیام بفرست.")

# پاسخ به همه پیام‌ها
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# مسیر دریافت پیام‌ها از تلگرام (Webhook)
@app.route("/", methods=["POST"])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid request', 403

# اجرای سرور روی پورت رندر
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
