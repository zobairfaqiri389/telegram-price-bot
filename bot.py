import os
import telebot
from flask import Flask, request

API_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(API_TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! لطفاً عکس محصول رو برام بفرست تا قیمت مناسبش رو پیدا کنم.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "عکس دریافت شد. (جستجوی قیمت در نسخه‌های بعدی اضافه می‌شود.)")

@server.route("/" + API_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get("RENDER_EXTERNAL_URL") + API_TOKEN)
    return "ربات راه‌اندازی شد!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
