from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types

def get_main_reply_keyboard():
    """Клавиатура внизу экрана (ReplyKeyboardMarkup)"""
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="📅 Дневной гороскоп"),
        types.KeyboardButton(text="📆 Недельный гороскоп")
    )
    builder.row(
        types.KeyboardButton(text="♈ Выбрать знак зодиака"),
        types.KeyboardButton(text="⚙️ Настройки")
    )
    return builder.as_markup(resize_keyboard=True)

def get_zodiac_inline_keyboard():
    """Инлайн-клавиатура для выбора знака зодиака"""
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="♈ Овен", callback_data="zodiac_aries"),
        types.InlineKeyboardButton(text="♉ Телец", callback_data="zodiac_taurus")
    )
    # ... остальные знаки
    return builder.as_markup()