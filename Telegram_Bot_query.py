import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with the API token you got from the BotFather
TOKEN = '5805760273:AAG-71QdKfiYKrCYQuXtic6_HPPz6OexmMY'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome to the Weather Bot! Type /weather <city> to get weather information.")

def get_weather(update: Update, context: CallbackContext) -> None:
    if not context.args:
        update.message.reply_text("Please provide a city name. Usage: /weather <city>")
        return

    city = " ".join(context.args)
    url = f"https://wttr.in/{city.replace(' ', '+')}?format=%C+%t+%w+%h+%v"

    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.text.strip().split(" ")
        
        condition = weather_data[0] if len(weather_data) >= 1 else "N/A"
        temperature = weather_data[1] if len(weather_data) >= 2 else "N/A"
        wind = weather_data[2] if len(weather_data) >= 3 else "N/A"
        humidity = weather_data[3] if len(weather_data) >= 4 else "N/A"
        visibility = weather_data[4] if len(weather_data) >= 5 else "N/A"

        weather_info = (
            f"Weather information for {city}:\n\n"
            f"Condition: {condition} {get_condition_emoji(condition)}\n"
            f"Temperature: {temperature}\n"
            f"Wind: {wind} {get_wind_emoji(wind)}\n"
            f"Humidity: {humidity} {get_humidity_emoji(humidity)}\n"
            f"Visibility: {visibility}\n"
        )

        update.message.reply_text(weather_info)
    else:
        update.message.reply_text("Failed to fetch weather data. Please try again later.")

def get_condition_emoji(condition):
    # Define emojis for different weather conditions
    emojis = {
        'Sunny': '☀️',
        'Rain': '🌧️',
        'Snow': '❄️',
        'Cloudy': '☁️',
        # Add more emojis for other conditions as needed
    }
    return emojis.get(condition, '')

def get_wind_emoji(wind):
    # Define emojis for different wind directions
    # You can customize this based on your preference
    return '🌬️'

def get_humidity_emoji(humidity):
    # Define emojis for different humidity levels
    # You can customize this based on your preference
    return '💧'

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("weather", get_weather))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
