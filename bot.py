import os
import telebot
from flask import Flask, request

API_TOKEN = os.environ.get("BOT_TOKEN")
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")  # مثل: https://telegram-price-bot-h2u9.onrender.com/
WEBHOOK_URL = f"{RENDER_URL}{API_TOKEN}"

bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام زبیر اینجاست! عکس محصولتو بفرست تا بررسی کنم.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("received_image.jpg", 'wb') as f:
        f.write(downloaded_file)
    bot.reply_to(message, "عکس دریافت شد. (پردازش قیمت در نسخه بعدی اضافه می‌شود)")

@server.route(f"/{API_TOKEN}", methods=['POST'])
def receive_update():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200

@server.route("/")
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    return "Webhook set", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
