from weather_api import OpenWeatherApi
from datetime import datetime


def format_weather_data(data):
    def convert_unix_time(unix_time):
        return datetime.utcfromtimestamp(unix_time).strftime('%H:%M')

    weather_summary = f"Сводка погоды для {data.get('name', 'Неизвестно')}:\n"

    weather_description = data['weather'][0]['description'] if 'weather' in data else 'Нет информации'
    temperature = round(data['main']['temp']) if 'main' in data and 'temp' in data['main'] else 'Нет информации'
    feels_like = round(data['main']['feels_like']) if 'main' in data and 'feels_like' in data['main'] else 'Нет информации'
    min_temp = round(data['main']['temp_min']) if 'main' in data and 'temp_min' in data['main'] else 'Нет информации'
    max_temp = round(data['main']['temp_max']) if 'main' in data and 'temp_max' in data['main'] else 'Нет информации'
    humidity = data['main']['humidity'] if 'main' in data and 'humidity' in data['main'] else 'Нет информации'
    wind_speed = data['wind']['speed'] if 'wind' in data and 'speed' in data['wind'] else 'Нет информации'
    sunrise = convert_unix_time(data['sys']['sunrise']) if 'sys' in data and 'sunrise' in data[
        'sys'] else 'Нет информации'
    sunset = convert_unix_time(data['sys']['sunset']) if 'sys' in data and 'sunset' in data['sys'] else 'Нет информации'

    weather_summary += f"Описание: {weather_description}\n"
    weather_summary += f"Температура: {temperature} градусов Цельсия (Ощущается как: {feels_like} градусов Цельсия)\n"
    weather_summary += f"Минимальная температура: {min_temp} градусов Цельсия, Максимальная температура: {max_temp} градусов Цельсия\n"
    weather_summary += f"Влажность: {humidity} процентов\n"
    weather_summary += f"Скорость ветра: {wind_speed} метров в секунду\n"
    weather_summary += f"Восход солнца: {sunrise}, Закат солнца: {sunset}\n"

    return weather_summary


def main(event, context):
    query_class = OpenWeatherApi("b3b7ebe39c95c5f0a9e893f32a7d576d")
    text = "Привет! Я расскажу тебе погоду, тебе всего лишь нужно назвать мне название своего города"
    if "request" in event and "original_utterance" in event["request"] and len(
            event["request"]["original_utterance"]) > 0:
        data = query_class.query_execution(0, "by_city_name", [event["request"]["original_utterance"], "RU"])
        text = format_weather_data(data)
    return {
        "version": event["version"],
        "session": event["session"],
        "response": {
            "text": text,
            "end_session": "false"
        }
    }