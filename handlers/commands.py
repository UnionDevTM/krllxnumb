# handlers/commands.py
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config.settings import settings

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    for sign in settings.ZODIAC_SIGNS:
        builder.add(types.InlineKeyboardButton(
            text=sign,
            callback_data=f"zodiac_{sign}"
        ))
    builder.adjust(3)

    await message.answer(
        "Укажите Ваш Знак Зодиака",
        reply_markup=builder.as_markup()
    )