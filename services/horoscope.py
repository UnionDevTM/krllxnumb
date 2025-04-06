import json
from config.settings import settings
from config.paths import HOROSCOPE_FOLDER
from functools import lru_cache

def get_horoscope(zodiac_sign: str) -> str:
    """Получает гороскоп для указанного знака"""
    try:
        if zodiac_sign not in settings.ZODIAC_SIGNS:
            return "Гороскоп для этого знака не найден"

        file_name = settings.ZODIAC_FILES.get(zodiac_sign)
        file_path = HOROSCOPE_FOLDER / file_name

        if not file_path.exists():
            return f"Файл с гороскопом {file_name} не найден"

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return data.get('data', {}).get('horoscope_data', 'Гороскоп не найден')

    except Exception as e:
        print(f"[ERROR] Ошибка при получении гороскопа: {e}")
        return "Произошла ошибка при получении гороскопа"




@lru_cache(maxsize=12)
def load_horoscope(file_path: str):
    """Загрузка гороскопа с кэшированием"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки {file_path}: {e}")
        return None