import time
import redis
import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

def get_weather(city):
    url = f"https://wttr.in/{city.replace(' ', '+')}?format=%C+%t+%w+%h+%v"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.text.strip().split(" ")
        condition = weather_data[0] if len(weather_data) >= 1 else "N/A"
        temperature = weather_data[1] if len(weather_data) >= 2 else "N/A"
        wind = weather_data[2] if len(weather_data) >= 3 else "N/A"
        humidity = weather_data[3] if len(weather_data) >= 4 else "N/A"
        visibility = weather_data[4] if len(weather_data) >= 5 else "N/A"
        weather_info = {
            "condition": condition,
            "temperature": temperature,
            "wind": wind,
            "humidity": humidity,
            "visibility": visibility,
        }
        return weather_info
    else:
        return None

@app.route('/')
def hello():
    count = get_hit_count()
    return f'Hello World! I have been seen {count} times.\n'

@app.route('/weather/<city>')
def show_weather(city):
    count = get_hit_count()
    weather_info = get_weather(city)
    if weather_info:
        return f'''
            Weather information for {city} (Accessed {count} times):\n\n
            Condition: {weather_info['condition']}\n
            Temperature: {weather_info['temperature']}\n
            Wind: {weather_info['wind']}\n
            Humidity: {weather_info['humidity']}\n
            Visibility: {weather_info['visibility']}\n
        '''
    else:
        return f"Failed to fetch weather data for {city}. Please try again later."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
