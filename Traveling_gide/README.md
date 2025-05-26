# Лаба по созданию туристической справки
> Тут что то более менее путное
## ТЗ
Написать на питоне код, который обращается к различным апишикам за данными:
1. В какую страну будет посещение (дать данные о столице и коде валюты)
2. Рассчитать сколько денег будет обменяно в путешествии при текущем курсе.
3. Берутся данные о погоде в отдельно взятом городе на ближайшие 5 дней (за объяснением [сюда](https://github.com/VladislaZyuzin/API-beginning/tree/main/Weather_2)).
## Выполнение
### Данные о стране
Для того, чтобы выполнить эту часть кода - необходимо обратиться к API, которая содержит информацию о странах на текущий момент времени. 

В результате поисков - я обратился к сайту: `restcountries.com`. Он даёт всю информацию о стране.

Из плюсов - тут не требуется ключь для получения данных, всё что нужно можно получить через определённые команды, с которыми можно ознакомиться в документации к API сайта.

Перейдём к первой части кода: 
```py
import requests  # Эта библиотека будет полезна при работе с многими API 

print("=====Туристическая справка=====\n")


def get_country():  # Метод, в котором мы через API обращаемся за инфой по странам
    while True:
        country = input("Введите страну на английском (или 'exit' для выхода): ").strip()    # .strip() - удаление лишних пробелов

        if country.lower() == 'exit':    # .lower() - защита от различных описаний 'exit'. Можно хоть капсом писать
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
            print(f"Столица: {capital}")
            currency_code = list(data[0]['currencies'].keys())[0]  # Эту команду следует запомнить, так как именно она даёт код валюты
            print(f"Код валюты: {currency_code}\n")
            return capital, currency_code
        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения: {e}. Проверьте интернет и попробуйте ещё раз.")
        except (KeyError, IndexError):
            print("Не удалось обработать данные страны. Попробуйте другое название.")  # Эта ситуация актуальна для Китая (КНР)
        except Exception as e:
            print(f"Неизвестная ошибка: {e}. Попробуйте ещё раз.")

```

Разбор команды `currency_code = list(data[0]['currencies'].keys())[0]`:
![image](https://github.com/user-attachments/assets/789355a0-aa61-49c2-952a-6645f7a8d623)

Как видно по коду, вывод представляет собой:
1. Столицу страны.
2. Код валюты.

### Пересчёт валюты в рубли.

Далее по ТЗ необходимо было получить данные о стоимости валюты в выбранной стране к рублю, для этого я воспользовался API: `api.exchangerate-api.com`. Она показывает актуальный курс валют. Как и предыдущий API - этот не требует ключа авторизованного пользователя.

Мой код выглядит следующим образом:
```py
def translation(currency_code):

    print("===Программа для рассчёта валюты===\n")

    while True:

        decision = input(f"Напишите 'да', если хотети продолжить или 'нет' если не хотите: \n")

        if decision.lower() == 'нет':
            print("Выход их программы...")
            return None, None

        elif decision.lower() == 'да':

            try:
                url = f"https://api.exchangerate-api.com/v4/latest/{currency_code}"
                response = requests.get(url)
                data = response.json()
                money = float(input(f"Введите количество рублей, которые вы возьмёте в поездку: "))

                abroad_curr = float(data['rates']['RUB'])    # Из интересного, воны КНДР не конвертируются в рубли :)
                common_ammount = money / abroad_curr

                print(f"Стоимость 1 {currency_code} составляет: {data['rates']['RUB']} рублей")
                print(f"Если вы возбмёте с собой {money} рублей, то вы сможете их поменять на {round(common_ammount, 2)} {currency_code}")
# {round(common_ammount, 2)}  - выводит значение с 2-мя цифрами после запятой

                return True

            except Exception as e:
                print(f"Неизвестная ошибка: {e}. Попробуйте ещё раз.")

        else:
            print("Неправильный ввод, попробуйте ещё раз")

```

Как видно в коде, при неправильном рассчёте у нас возникает бесконечный цикл, который можно остановить либо при правильном вводе данных или при вводе "нет".

### Поиск прогноза погоды

Всё объяснение идёт по ссылке в начале. Таким образом у меня выглядит код для данной работы: 
```py
def weather():
    while True:
        print("\n===Прогноз погоды на 5 дней===")
        city = input("Введите город (ввод по-русски) либо нажмите 'exit': ").strip()
        print(f"\nПрогноз погоды на 5 дней для города: {city}")
        if city.lower() == 'exit':
            print("Выход из программы...")
            return None, None
        try:
                api_key_for_weather = "ТУТ ВВОДИТЕ СВОЙ КЛЮЧ"
            url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key_for_weather}&units=metric&lang=ru'
            response = requests.get(url)
            data = response.json()
            printed_dates = {}
            target_times = ["09:00:00", "15:00:00", "21:00:00"]
            for forecast in data['list']:
                dt_txt = forecast['dt_txt']
                date_str, time = dt_txt.split()  # Разделяем дату и время

                # Если это одно из нужных нам времени
                if time in target_times:
                    if date_str not in printed_dates:
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

        except requests.exceptions.RequestException as e:
            print(f"Ошибка подключения: {e}. Проверьте интернет и попробуйте ещё раз.")
        except (KeyError, IndexError):
            print("Не удалось обработать данные страны. Попробуйте другое название.")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}. Попробуйте ещё раз.")
```
### Вызов функций

В конце - требуется вывести все функции таким образом, чтобы при нежелании пользователся пользоваться дальнейшим функионалом приложения - он мог спокойно завершить работу и следующие скрипты не выполнялись.

Для этого введём вызовы и условия при которых можно вызывать следующие методы: 
```py
capital, currency = get_country()    # По условию первого метода - нам должны вернуться данные о столице и валюте

if capital is None:
    exit()    # если данные не вернулись, то работа завершается (случай с 'exit')


if translation(currency) is not True:    # Для метода translation требутся инфа о валюте, котрая должна вернуться по окончанию работы предыдущего метода.
# Если пользователь не захочет взаимодействовать с этим методом, то он завершится и скрипт следующего метода не запустится
    exit()

weather()
```

### Результат работы

![image](https://github.com/user-attachments/assets/3cb31666-23cc-4c55-b1f6-b65b7493ea1e)

![image](https://github.com/user-attachments/assets/f83af32f-24c4-4a6e-bb44-c5ebe2024a37)

![image](https://github.com/user-attachments/assets/29551cbc-57e9-49e1-970d-9903b4c430f3)

## Заключение
Работа по API была выполнена, были задействованы все моменты, которые требовались в ТЗ и реализованы в моей лабе. 
