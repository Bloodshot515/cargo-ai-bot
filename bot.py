import telebot
import os

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я готов работать.")

@bot.message_handler(commands=['погода'])
def weather(message):
    bot.reply_to(message, "Сегодня солнечно, +25°C")

@bot.message_handler(commands=['топливо'])
def fuel(message):
    bot.reply_to(message, "Средняя цена дизеля: $3.78")

@bot.message_handler(commands=['ставка'])
def rate(message):
    bot.reply_to(message, "Ставка по региону: $0.92/миля")

bot.polling()