
import telebot
import os

TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Бот работает корректно.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, "Вы написали: " + message.text)

bot.polling(non_stop=True)
