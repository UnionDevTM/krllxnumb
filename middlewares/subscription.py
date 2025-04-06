from aiogram import types
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from config.settings import settings
from typing import Callable, Awaitable, Dict, Any


class SubscriptionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[types.TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: types.TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        # Пропускаем проверку для команд /start и /help
        if isinstance(event, types.Message) and event.text in ['/start', '/help']:
            return await handler(event, data)

        # Проверяем подписку для всех остальных событий
        bot = data['bot']
        user_id = event.from_user.id

        try:
            member = await bot.get_chat_member(
                chat_id=settings.CHANNEL_USERNAME,
                user_id=user_id
            )
            is_subscribed = member.status in ['member', 'administrator', 'creator']

            if not is_subscribed:
                if isinstance(event, types.CallbackQuery):
                    await event.answer(
                        "Для использования бота подпишитесь на канал!",
                        show_alert=True
                    )
                    return
                elif isinstance(event, types.Message):
                    await event.answer(
                        "Пожалуйста, подпишитесь на наш канал для доступа к боту:\n"
                        f"👉 {settings.CHANNEL_USERNAME}",
                        disable_web_page_preview=True
                    )
                    return

        except Exception as e:
            print(f"Ошибка проверки подписки: {e}")
            # В случае ошибки пропускаем проверку
            pass

        return await handler(event, data)