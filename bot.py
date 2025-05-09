import os
import telebot
from flask import Flask, request

# دریافت توکن و آدرس webhook از متغیرهای محیطی
API_TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # مثلاً https://telegram-price-bot-h2u9.onrender.com/webhook

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

# پاسخ به پیام‌های /start
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "سلام! ربات با موفقیت فعاله. لطفاً عکس یا پیام بفرست.")

# مسیر webhook که تلگرام پیام‌ها رو بهش می‌فرسته
@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode('utf-8'))
    bot.process_new_updates([update])
    return 'OK', 200

# فقط برای تست ربات روی دامنه اصلی
@app.route('/')
def index():
    return 'ربات فعاله', 200

# تنظیم webhook هنگام اجرا
if __name__ == '__main__':
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
