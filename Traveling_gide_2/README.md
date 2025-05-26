# Тревел лаба 2.0.
> Тут я уже много чего сделал, надеюсь, если ты HR, то тут ты получишь кайфы :)
## ТЗ
Задача данной лабы - улучшить предыдущий код ([ссылочка тут](https://github.com/VladislaZyuzin/API-beginning/tree/main/Traveling_gide)) таким образом, чтобы:
1. Были советы об одежде при определённой погоде.
2. Появился словарь данных, сохраняющий данные о рассчёте валюты
3. Сохранение запросов в файлы.
## Выполнение задачи: 
### Подбор одежды

Для того, чтобы создать советы по одежде - нам следует сделать необходимый для этого метод, который будет встроен в метод `weather`. 

Для этого был написан следующий код: 
```py
def weather():
    city = input("\nВведите город (по-русски) или 'exit': ").strip()
    if city.lower() == 'exit':
        print("Выход из системы...")
        return None

    print("\n===Прогноз погоды на 5 дней===")
    try:
        api_key_for_weather = "b9e91632854834d94ac5fcb020abbd48"
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key_for_weather}&units=metric&lang=ru'
        response = requests.get(url)
        data = response.json()
        printed_dates = {}
        target_times = ["09:00:00", "15:00:00", "21:00:00"]
        weather_data = []

        def clothing_advice(tempe):
            if tempe > 25:
                return "🥵 Жарко: футболка, шорты, панама, солнцезащитные очки"
            elif 15 <= tempe <= 25:
                return "😊 Тепло: лёгкая куртка, джинсы"
            elif 0 <= tempe < 15:
                return "❄️ Холодно: пальто, шапка, перчатки"
            else:
                return "🧊 Мороз: пуховик, термобельё, шарф"
        for forecast in data['list']:
            dt_txt = forecast['dt_txt']
            date_str, time = dt_txt.split()  # Разделяем дату и время

        # Если это одно из нужных нам времени
            if time in target_times:
                print(f"\n==={date_str}===")
                printed_dates[date_str] = True

                temp = forecast['main']['temp']
                weather = forecast['weather'][0]['description']
                wind = forecast['wind']['speed']
                sea_level = forecast['main'].get('sea_level', 'N/A')
                emoji = {
                    "ясно": "☀️",
                    "дождь": "🌧️",
                    "небольшой дождь": "🌧️",
                    "пасмурно": "☁️",
                    "небольшая облачность": "☁️",
                    "переменная облачность": "☁️",
                    "облачно с прояснениями": "🌥️"
                }.get(weather, " ")

                print(f"Прогноз погоды в городе {city}")
                print(f"{time[:5]} - Температура: {temp}°C, {weather.capitalize()}, {emoji}")
                print(f"   Ветер: {wind} м/с, Уровень моря: {sea_level}")
                print(f"   Рекомендации: {clothing_advice(temp)}")  # Выводим советы

                weather_data.append({
                    "date": date_str,
                    "time": time[:5],
                    "temp": temp,
                    "weather": weather,
                    "wind": wind,
                    "sea level": sea_level,
                    "clothing_advice": clothing_advice(temp)
                })

        return {"city": city, "forecasts": weather_data}

    except requests.exceptions.RequestException as e:
        print(f"Ошибка подключения: {e}. Проверьте интернет и попробуйте ещё раз.")
    except (KeyError, IndexError):
        print("Не удалось обработать данные страны. Попробуйте другое название.")
    except Exception as e:
        print(f"Неизвестная ошибка: {e}. Попробуйте ещё раз.")
```
Как видно по коду: 
1. Был включен метод по подбору одежды по погоде: `clothing_advice(tempe)`.
2. Для него составлены необходимые команды для корректного вывода
3. Был составлен список: `weather_data.append` для дальнейшего внесения записей о запросе в файловую систему.
4. Так же, внутренние методы ни в коем случае нельзя писать внутри цикла, иначе вывод будет некорректным.

### Сохранение данных о пересчёте рублей в иностранные валюты.

Для этого был создан список: `exchange_history = []` и до бесконечного цикла добавлен метод `show_history()`.

Снизу представлен код с ключевыми изменениями: 

```py
exchange_history = []


def translation(currency_code):
    print("===Программа для рассчёта валюты===\n")

    def show_history():
        for item in exchange_history:
            print(f"{item['amount_rub']} RUB → {item['result']} {item['currency']}")

    while True:

        decision = input(f"Напишите 'да', если хотети продолжить или 'нет' если не хотите: \n")
        if decision.lower() == 'нет':
            print("Выход их программы...")
            return exchange_history if exchange_history else None
        elif decision.lower() == 'да':

            try:
                url = f"https://api.exchangerate-api.com/v4/latest/{currency_code}"
                response = requests.get(url)
                data = response.json()
                money = float(input(f"Введите количество рублей, которые вы возьмёте в поездку: "))

                abroad_curr = float(data['rates']['RUB'])
                common_ammount = money / abroad_curr
                exchange_history.append({
                    "currency": currency_code,
                    "amount_rub": money,
                    "result": round(common_ammount, 2)
                })

                print(f"Стоимость 1 {currency_code} составляет: {data['rates']['RUB']} рублей")
                print(
                    f"Если вы возбмёте с собой {money} рублей, то вы сможете их поменять на {round(common_ammount, 2)} {currency_code}")

                show_history()

            except Exception as e:
                print(f"Неизвестная ошибка: {e}. Попробуйте ещё раз.")

        else:
            print("Неправильный ввод, попробуйте ещё раз")
```
Как видно, метод получил больше нужных команд и теперь он может: 
1. Вызвращать историю обмена для дальнейшего хранения.
2. Показывать эту историю.
### Сохранение отчёта в файл
Самое трудоёмкое было составить код для сохранения данных. Для этого был написан метод `save_report`. Код представлен ниже: 
```py
def save_report(country, capital, exchange_data, weather_data):
    if not all([country, capital, exchange_data, weather_data]):
        print("Недостаточно данных для отчёта!")
        return

    report = {
        "country": country,
        "capital": capital,
        "exchange_rates": exchange_data,
        "weather": weather_data,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    filename = f"{country}_travel_report.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    print(f"\nОтчёт сохранён в файл: {filename}")
```
В данном коде мы берём все данные по методам: страны, валюты и погоды для сохранения в создавшийся json файл. Стоит обратить внимание на некоторые команды: 
```py
    filename = f"{country}_travel_report.json"  # Тут создаём имя файла в зависимости от страны
    with open(filename, "w", encoding="utf-8") as f:
# with - менеджер контекста (автоматически закрывает файл после блока)
# "w" - файл открывается для записи (перезаписывается если существует)
# encoding="utf-8" - кодировка для корректного сохранения кириллицы
# f - файловый объект (дескриптор файла)
        json.dump(report, f, indent=4, ensure_ascii=False)
# json.dump() - сериализует Python-объект в JSON-формат
# report - словарь с данными для сохранения
# f - файловый объект для записи
# indent=4 - красивое форматирование с отступами (4 пробела)
# ensure_ascii=False - сохраняет кириллицу как есть (без \u-последовательностей)
    print(f"\nОтчёт сохранён в файл: {filename}")
```
Т.о был составлен данный файл для сохранения данных. 

## Результат работы

![image](https://github.com/user-attachments/assets/c98bcfdb-8fe3-4a62-a2f0-4c6c3973dd92)

![image](https://github.com/user-attachments/assets/88039a53-dcbe-4d1a-a6c5-fb0a97e71081)

![image](https://github.com/user-attachments/assets/afb374a6-522c-4efc-af14-53f34a1bbf58)

![image](https://github.com/user-attachments/assets/53615884-4b2d-4899-b0c0-4c69525d2782)

## Заключение

Я уже что то научился делать, так что всё ок, мб, кому то это будет полезным. Кстати, в общем коде, который находится **ССЫЛКА** представлены некоторые другие изменения, о которых не было обговорено из-за интуитивной понятности. 



