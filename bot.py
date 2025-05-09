
import telebot
import requests
from bs4 import BeautifulSoup

TOKEN = "8129606302:AAGQ1TbMqBQqqE-CG4nWFaNtldguwYGIlUU"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    file = bot.download_file(file_info.file_path)
    with open("temp.jpg", 'wb') as f:
        f.write(file)
    bot.reply_to(message, "عکس دریافت شد. (در این نسخه، جستجو انجام نمی‌شود.)")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام! عکس محصول را بفرست تا قیمتش را پیدا کنم.")

bot.polling()
