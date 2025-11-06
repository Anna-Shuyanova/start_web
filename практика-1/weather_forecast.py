import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Получаем API ключ из переменных окружения
API_KEY = os.getenv('OPENWEATHER_API_KEY')

if not API_KEY:
    print("❌ Ошибка: API ключ не найден. Проверьте файл .env")
    exit(1)

def get_weather_forecast(city_name, units="metric"):
    """
    Получает прогноз погоды на 5 дней
    """
    base_url = "http://api.openweathermap.org/data/2.5/forecast"
    
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': units,
        'lang': 'ru'
    }
    
    try:
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return {"error": "Город не найден"}
        else:
            return {"error": f"Ошибка API: {response.status_code}"}
            
    except requests.exceptions.ConnectionError:
        return {"error": "Не удалось подключиться к серверу"}
    except Exception as e:
        return {"error": f"Произошла ошибка: {str(e)}"}

def display_forecast(forecast_data, units="metric"):
    """
    Отображает прогноз погоды
    """
    if "error" in forecast_data:
        print(f"❌ {forecast_data['error']}")
        return
    
    city = forecast_data['city']['name']
    country = forecast_data['city']['country']
    
    print(f"\n📅 Прогноз погоды на 5 дней для {city}, {country}")
    print("="*60)
    
    # Группируем прогноз по дням
    daily_forecasts = {}
    
    for item in forecast_data['list']:
        date = item['dt_txt'].split()[0]  # Получаем только дату
        if date not in daily_forecasts:
            daily_forecasts[date] = []
        daily_forecasts[date].append(item)
    
    # Выводим прогноз по дням
    for date, forecasts in list(daily_forecasts.items())[:5]:  # Ограничиваем 5 днями
        # Берем прогноз на обеденное время (12:00) для простоты
        midday_forecast = None
        for forecast in forecasts:
            if "12:00:00" in forecast['dt_txt']:
                midday_forecast = forecast
                break
        
        # Если нет прогноза на 12:00, берем первый доступный
        if not midday_forecast:
            midday_forecast = forecasts[len(forecasts)//2]  # берем средний прогноз дня
        
        # Форматируем дату
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        day_names = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        day_name = day_names[date_obj.weekday()]
        formatted_date = date_obj.strftime(f"%d.%m.%Y ({day_name})")
        
        temp = midday_forecast['main']['temp']
        desc = midday_forecast['weather'][0]['description']
        humidity = midday_forecast['main']['humidity']
        wind_speed = midday_forecast['wind']['speed']
        
        temp_unit = "°C" if units == "metric" else "°F"
        speed_unit = "м/с" if units == "metric" else "миль/ч"
        
        print(f"📅 {formatted_date}")
        print(f"   🌡️  {temp}{temp_unit} | ☁️  {desc.capitalize()}")
        print(f"   💧 Влажность: {humidity}% | 💨 Ветер: {wind_speed} {speed_unit}")
        print()

def main():
    print("📅 Прогноз погоды OpenWeatherMap")
    print("="*35)
    
    while True:
        city = input("\nВведите название города (или 'выход' для завершения): ").strip()
        
        if city.lower() in ['выход', 'exit', 'quit']:
            print("До свидания! 👋")
            break
            
        if not city:
            print("⚠️  Пожалуйста, введите название города")
            continue
    
        units_choice = input("Выберите единицы измерения (1 - метрические, 2 - имперские): ").strip()
        units = "imperial" if units_choice == "2" else "metric"
        
        print("\n⏳ Запрашиваю прогноз погоды...")
        
        forecast_data = get_weather_forecast(city, units)
        display_forecast(forecast_data, units)

if __name__ == "__main__":
    main()