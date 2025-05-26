import requests
import json
from datetime import datetime

print("=====Туристическая справка=====\n")


def get_country():
    while True:
        country = input("Введите страну на английском (или 'exit' для выхода): ").strip()

        if country.lower() == 'exit':
            print("Выход из программы... ")
            return None, None

        try:
            url = f"https://restcountries.com/v3.1/name/{country}"
            response = requests.get(url)

            # Проверяем статус ответа
            if response.status_code == 404:
                print("Страна не найдена. Попробуйте ещё раз.")
                continue

            response.raise_for_status()  # Проверяем другие HTTP-ошибки

            data = response.json()
            capital = data[0]['capital'][0]
            print(f"\nСтрана: {country.title()}")
            print(f"Столица: {capital}")
            currency_code = list(data[0]['currencies'].keys())[0]
            print(f"Код валюты: {currency_code}\n")
            return capital, currency_code, country

        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения: {e}. Проверьте интернет и попробуйте ещё раз.")
        except (KeyError, IndexError):
            print("Не удалось обработать данные страны. Попробуйте другое название.")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}. Попробуйте ещё раз.")


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


capital, currency, country = get_country()
if not country:
    exit()

exchange_data = translation(currency)
if not exchange_data:
    exit()

weather_data = weather()
if not weather_data:
    exit()

save_report(country, capital, exchange_data, weather_data)
