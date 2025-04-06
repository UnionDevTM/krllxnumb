# services/storage.py
from datetime import datetime
import json
from pathlib import Path
from config.paths import DATA_FILE

METRICS_DIR = Path("data/metrics")

def ensure_data_file():
    """Создает файл данных, если его нет"""
    if not DATA_FILE.exists():
        DATA_FILE.write_text('{}', encoding='utf-8')


def update_user_data(user_id: int, data_type: str = None, value=None):
    """Обновляет данные пользователя"""
    ensure_data_file()
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        user_key = str(user_id)
        if user_key not in data:
            data[user_key] = {}

        if data_type is not None:
            data[user_key][data_type] = value

        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Ошибка сохранения данных: {e}")


def get_user_data(user_id: int) -> dict:
    """Получает данные пользователя"""
    ensure_data_file()
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f).get(str(user_id), {})
    except Exception as e:
        print(f"Ошибка чтения данных: {e}")
        return {}

def track_metric(user_id: int, metric_name: str, data: dict = None):
    """Сохраняет метрику в файл"""
    METRICS_DIR.mkdir(exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    metric_file = METRICS_DIR / f"{metric_name}_{today}.json"

    record = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        **data
    }

    # Добавляем в существующий файл или создаем новый
    try:
        with open(metric_file, "r+", encoding="utf-8") as f:
            existing = json.load(f)
            existing.append(record)
            f.seek(0)
            json.dump(existing, f)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(metric_file, "w", encoding="utf-8") as f:
            json.dump([record], f)