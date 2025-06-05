
import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "3407928623134a78febd827ae255da69")

CITIES = {
    "New York": (40.7128, -74.0060),
    "Chicago": (41.8781, -87.6298),
    "Houston": (29.7604, -95.3698),
    "Los Angeles": (34.0522, -118.2437),
    "Atlanta": (33.7490, -84.3880),
    "Philadelphia": (39.9526, -75.1652),
    "Miami": (25.7617, -80.1918),
    "Phoenix": (33.4484, -112.0740),
    "Denver": (39.7392, -104.9903),
    "Seattle": (47.6062, -122.3321)
}

START_RATES = {
    "Laredo, TX": 0.70,
    "Chicago, IL": 1.01,
    "Newark, NJ": 0.98,
    "Atlanta, GA": 0.93,
    "Los Angeles, CA": 0.75,
    "Houston, TX": 0.80,
    "Miami, FL": 0.85
}

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    messages = []
    for city, (lat, lon) in CITIES.items():
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=imperial"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            temp = data['main']['temp']
            wind = data['wind']['speed']
            weather = data['weather'][0]['main']
            messages.append(f"{city}: {temp}°F, {weather}, Wind {wind} mph")
    await update.message.reply_text("\n".join(messages))

async def fuel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fuel_prices = {
        "New York": "Diesel: $3.95 | Gas: $3.59",
        "Chicago": "Diesel: $3.89 | Gas: $3.47",
        "Houston": "Diesel: $3.72 | Gas: $3.35",
    }
    messages = [f"{city}: {price}" for city, price in fuel_prices.items()]
    await update.message.reply_text("\n".join(messages))

async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from datetime import datetime
    day = (datetime.now() - datetime(datetime.now().year, 1, 1)).days + 1
    messages = []
    for city, base in START_RATES.items():
        rate = base + 0.01 * (day // 3) - 0.01 * (day % 11 == 0)
        rate = max(rate, 0.65)
        messages.append(f"{city}: ${rate:.2f} per mile")
    await update.message.reply_text("\n".join(messages))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("fuel", fuel))
    app.add_handler(CommandHandler("rate", rate))
    app.run_polling()
