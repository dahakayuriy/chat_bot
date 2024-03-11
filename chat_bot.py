from telegram.ext import Updater, CommandHandler, MessageHandler, filters, Application, ContextTypes
from telegram import ForceReply, Update, ReplyKeyboardMarkup, KeyboardButton
from datetime import datetime
import requests


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! What would you like to do?",
        reply_markup=get_main_keyboard(),
    )


async def get_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    current_time = datetime.now().strftime("%H:%M:%S")
    await update.message.reply_text(f"The current time is {current_time}")


async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    api_key = "52c21fe31e7f190b1c89a1b6f2f58972"
    city = "Mykolaiv"  # Замініть CityName на назву міста, для якого ви хочете отримати погоду

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        weather_message = f"The weather in {city} is {weather_description}. Temperature: {temperature}°C, Humidity: {humidity}%, Wind Speed: {wind_speed} m/s"
    else:
        weather_message = "Failed to fetch weather data"

    await update.message.reply_text(weather_message)


def get_main_keyboard():
    keyboard = [
        [KeyboardButton("/start"), KeyboardButton("/time"),
         KeyboardButton("/weather")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# def echo(update,context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
application = Application.builder().token(
    "6630370844:AAFnNVKpf_9-cMghEhJPDtErV5enigvud40").build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("time", get_time))
application.add_handler(CommandHandler("weather", get_weather))
# message_handler = MessageHandler(filters.text & ~filters.command,echo)
application.run_polling(allowed_updates=Update.ALL_TYPES)
