# handlers/callbacks.py

from aiogram import Router, types, F
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config.settings import settings
from services.storage import update_user_data, get_user_data
from pathlib import Path
from functools import lru_cache
import logging
import json

router = Router()

# Укажите правильный путь к папке с гороскопами
HOROSCOPES_DIR = Path(r"C:\Users\User\PycharmProjects\PythonProject\krllxnumb\parser\updatehoro\horoscopes")
HOROSCOPESWEEK_DIR = Path (r"C:\Users\User\PycharmProjects\PythonProject\krllxnumb\parser\updatehoro\horoscopeweekly")


@router.callback_query(F.data.startswith("zodiac_"))
async def process_zodiac(callback: types.CallbackQuery):
    zodiac_sign = callback.data.split("_", maxsplit=1)[1]
    if zodiac_sign not in settings.ZODIAC_SIGNS:
        await callback.answer("Неизвестный знак зодиака!", show_alert=True)
        return

    user = callback.from_user
    user_id = user.id
    update_user_data(user_id, "zodiac", zodiac_sign)

    # Создаем клавиатуру для отображения ПОД сообщением
    builder = InlineKeyboardBuilder()

    # Первый ряд кнопок
    builder.row(
        types.InlineKeyboardButton(
            text="📅 Daily horoscope",  # Эмодзи для наглядности
            callback_data="horoscope_daily"
        )
    )

    # Второй ряд кнопок
    builder.row(
        types.InlineKeyboardButton(
            text="📆 Weekly horoscope",
            callback_data="horoscope_weekly"
        )
    )

    # Третий ряд кнопок
    builder.row(
        types.InlineKeyboardButton(
            text="👣 Digital footprint",
            callback_data="digital_footprint"
        ),
        types.InlineKeyboardButton(
            text="⚙️ Settings",
            callback_data="open_settings"
        )
    )

    nickname = user.first_name or "Пользователь"
    if user.last_name:
        nickname += f" {user.last_name}"

    # Отправляем сообщение с клавиатурой ПОД текстом
    await callback.message.edit_text(
        text=f"{nickname}, Ваш знак зодиака: {zodiac_sign}",
        reply_markup=builder.as_markup()
    )
    await callback.answer()


@router.callback_query(F.data == "open_settings")
async def open_settings(callback: types.CallbackQuery):
    # Вызываем обработчик команды /start
    from handlers.commands import cmd_start
    await cmd_start(callback.message)
    await callback.answer()

# Добавляем кэширующую функцию для загрузки гороскопов
@lru_cache(maxsize=12)  # Кэшируем 12 знаков зодиака
def load_horoscope(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Ошибка загрузки гороскопа: {e}")
        return None

@router.callback_query(F.data == "horoscope_daily")
async def daily_horoscope(callback: types.CallbackQuery):
    user_data = get_user_data(callback.from_user.id)
    zodiac_sign = user_data.get("zodiac")

    if not zodiac_sign:
        await callback.answer("Сначала выберите знак зодиака!", show_alert=True)
        return

    file_name = settings.ZODIAC_FILES.get(zodiac_sign)
    if not file_name:
        await callback.answer("Ошибка: знак зодиака не найден", show_alert=True)
        return

    file_path = HOROSCOPES_DIR / file_name

    try:
        horoscope_data = load_horoscope(file_path)  # Используем кэшированную функцию
        horoscope_text = horoscope_data.get('data', {}).get('horoscope_data', 'Гороскоп не найден')

        # Добавляем рекламу или премиум-контент
        premium_text = "\n\n🔮 Хотите подробный гороскоп? /premium"

        await callback.message.answer(
            f"🎊 Daily Horoscope for {zodiac_sign} 🎊\n\n"
            f"{horoscope_text}"
            f"{premium_text if not user_data.get('is_premium') else ''}"
        )

    except Exception as e:
        logging.error(f"Ошибка при отправке гороскопа: {e}")
        await callback.answer("Произошла ошибка", show_alert=True)

    await callback.answer()


@router.callback_query(F.data == "horoscope_weekly")
async def weekly_horoscope(callback: types.CallbackQuery):
    try:
        user_data = get_user_data(callback.from_user.id)
        zodiac_sign = user_data.get("zodiac")


        if not zodiac_sign:
            await callback.answer("Сначала выберите знак зодиака!", show_alert=True)
            return

        file_name = settings.ZODIAC_FILES.get(zodiac_sign)
        if not file_name:
            await callback.answer("Ошибка: знак зодиака не найден", show_alert=True)
            return

        file_path = str((HOROSCOPESWEEK_DIR / file_name).absolute())

        if not Path(file_path).exists():
            await callback.answer("Гороскоп временно недоступен", show_alert=True)
            return

        horoscope_data = load_horoscope(file_path)
        if not horoscope_data:
            await callback.answer("Ошибка загрузки гороскопа", show_alert=True)
            return

        premium_text = "\n\n🔮 Хотите подробный гороскоп? /premium" if not user_data.get('is_premium') else ""

        await callback.message.answer(
            f"🎊 Weekly Horoscope for {zodiac_sign} 🎊\n\n"
            f"{horoscope_data.get('data', {}).get('horoscope_data', 'Гороскоп не найден')}"
            f"{premium_text}"
        )

    except Exception as e:
        logging.error(f"Ошибка в weekly_horoscope: {e}", exc_info=True)
        await callback.answer("Произошла непредвиденная ошибка", show_alert=True)
    finally:
        await callback.answer()



@router.callback_query(F.data == "digital_footprint")
async def digital_footprint(callback: types.CallbackQuery):
    # Логика для цифрового следа
    await callback.answer("Функция цифрового следа в разработке", show_alert=True)

from handlers.keyboards import get_zodiac_inline_keyboard

@router.callback_query(F.data == "choose_zodiac")
async def choose_zodiac(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Выберите знак зодиака:",
        reply_markup=get_zodiac_inline_keyboard()
    )