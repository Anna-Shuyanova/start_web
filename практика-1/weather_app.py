import requests
from pprint import pprint
import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Получаем API ключ из переменных окружения
API_KEY = os.getenv('OPENWEATHER_API_KEY')

if not API_KEY:
    print("❌ Ошибка: API ключ не найден. Проверьте файл .env")
    exit(1)

def get_current_weather(city_name, units="metric"):
    """
    Получает текущую погоду для указанного города
    """
    # Базовый URL для API текущей погоды
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Параметры запроса
    params = {
        'q': city_name,
        'appid': API_KEY,
        'units': units,  # metric - Цельсий, imperial - Фаренгейт
        'lang': 'ru'     # для получения описания на русском
    }
    
    try:
        # Отправляем GET-запрос
        response = requests.get(base_url, params=params)
        
        # Проверяем статус ответа
        if response.status_code == 200:
            # Успешный запрос
            data = response.json()
            return data
        elif response.status_code == 404:
            # Город не найден
            return {"error": "Город не найден"}
        else:
            # Другие ошибки
            return {"error": f"Ошибка API: {response.status_code}"}
            
    except requests.exceptions.ConnectionError:
        return {"error": "Не удалось подключиться к серверу"}
    except Exception as e:
        return {"error": f"Произошла ошибка: {str(e)}"}

def display_weather(weather_data, units="metric"):
    """
    Красиво отображает данные о погоде
    """
    if "error" in weather_data:
        print(f"❌ {weather_data['error']}")
        return
    
    # Извлекаем данные
    city = weather_data['name']
    country = weather_data['sys']['country']
    temp = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    humidity = weather_data['main']['humidity']
    weather_desc = weather_data['weather'][0]['description']
    wind_speed = weather_data['wind']['speed']
    
    # Определяем единицы измерения
    temp_unit = "°C" if units == "metric" else "°F"
    speed_unit = "м/с" if units == "metric" else "миль/ч"
    
    # Выводим информацию
    print("\n" + "="*50)
    print(f"🌍 Погода в {city}, {country}")
    print("="*50)
    print(f"🌡️  Температура: {temp}{temp_unit} (ощущается как {feels_like}{temp_unit})")
    print(f"☁️  Описание: {weather_desc.capitalize()}")
    print(f"💧 Влажность: {humidity}%")
    print(f"💨 Скорость ветра: {wind_speed} {speed_unit}")
    print("="*50)

def main():
    print("🌤️  Погодное приложение OpenWeatherMap")
    print("="*35)
    
    while True:
        # Запрашиваем город у пользователя
        city = input("\nВведите название города (или 'выход' для завершения): ").strip()
        
        if city.lower() in ['выход', 'exit', 'quit']:
            print("До свидания! 👋")
            break
            
        if not city:
            print("⚠️  Пожалуйста, введите название города")
            continue
        
        # Запрашиваем единицы измерения
        units_choice = input("Выберите единицы измерения (1 - метрические, 2 - имперские): ").strip()
        units = "imperial" if units_choice == "2" else "metric"
        
        print("\n⏳ Запрашиваю данные о погоде...")
        
        # Получаем данные о погоде
        weather_data = get_current_weather(city, units)
        
        # Отображаем результат
        display_weather(weather_data, units)

if __name__ == "__main__":
    main()