import requests
import json
import os

# Список всех знаков зодиака
zodiac_signs = [
    "aries", "taurus", "gemini", "cancer",
    "leo", "virgo", "libra", "scorpio",
    "sagittarius", "capricorn", "aquarius", "pisces"
]

# Папка для сохранения файлов (создаётся автоматически)
output_folder = "horoscopeweekly"
os.makedirs(output_folder, exist_ok=True)


def save_horoscopeweekly():
    for sign in zodiac_signs:
        try:
            # Запрос к API
            url = f"https://horoscope-app-api.vercel.app/api/v1/get-horoscope/weekly?sign={sign}"
            response = requests.get(url)
            response.raise_for_status()

            # Получаем данные
            data = response.json()

            # Формируем имя файла
            filename = f"{output_folder}/{sign}.json"

            # Сохраняем в JSON с отступами
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"✅ Гороскоп для {sign} сохранён в {filename}")

        except Exception as e:
            print(f"❌ Ошибка для {sign}: {str(e)}")


if __name__ == "__main__":
    save_horoscopeweekly()
    print("\nВсе недельные гороскопы сохранены в папке 'horoscopeweekly'!")