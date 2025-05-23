# Лаба 2 по API
## ТЗ 
Найти данные по прогнозу погоды на ближайшие 5 дней по Питеру. Данные должны быть на утро, день, вечер.
## Выполнение
В данной лабораторной работе мною был организован поиск прогноза погоды через API на питоне. Благодаря моему коду и библиотеке `requests`. Мне удалось получить необходимые данные. Ниже рассмотрен код с комментами: 
```py
from datetime import date
import requests    #Эта библиотека больше всего нужна

api_key = "b9e91632854834d94ac5fcb020abbd48"
city = "Санкт-Петербург"
url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=ru'

response = requests.get(url)  # Команда get позволяет получить инфу с указанного URL адреса.
# Пайчарм через интернет и апи передаёт запрос на сайт openweathermap и оттуда получается ответ
data = response.json()  # Тут получаем данные от запроса в формате json
# Для проверки рекомендую ввести команду: print(data) так будет понятнее какую инфу доставать в дальнейшем

print(f"Прогноз погоды в {city} на 5 дней")

target_times = ["09:00:00", "15:00:00", "21:00:00"]
printed_dates = {}    # Для того, чтобы не повторяться - сделаем словарь, в дальнейшем он понадобится для того, чтобы некоторые наши данные не повторялись


def weather_at_1st(weather_data):  # Можно без метода, но я забыл всё про прогу, поэтому - пускай будет.
    for forecast in weather_data['list']:    
        dt_txt = forecast['dt_txt']    # Тут берём инфу только о погоде днём из списка data
        date_str, time = dt_txt.split()  # Разделяем дату и время

        # Если это одно из нужных нам времени
        if time in target_times:
            if date_str not in printed_dates:
                print(f"\n==={date_str}===")
                printed_dates[date_str] = True    # Тут мы записываем в нашем случае дни, чтобы они не повторялись. 

            # Ниже расписано то, что нам требуется найти, как написано ранее - мы из json файла вынимаем то, что нам нужно по погоде.
            temp = forecast['main']['temp']
            weather = forecast['weather'][0]['description']
            wind = forecast['wind']['speed']
            sea_level = forecast['main'].get('sea_level', 'N/A')

            print(f"{time[:5]} - Температура: {temp}°C, {weather.capitalize()}")
            # time[:5] - это, чтобы в выводе у нас было не 09:00:00, а 09:00
            # weather.capitalize() - чтобы первая бука в выводе про погоду была заглавной
            print(f"   Ветер: {wind} м/с, Уровень моря: {sea_level}")


weather_at_1st(data)
```
