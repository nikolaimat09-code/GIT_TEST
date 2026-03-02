"""
Простой эхо-бот на aiogram 3.
Повторяет обратно любое текстовое сообщение пользователя.

Токен берётся из переменной BOT_TOKEN в .env.
Запуск: python bot.py

Команды:
- /start — приветствие
- любой текст — бот ответит тем же текстом (эхо)
"""
import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Подгружаем переменные из .env (BOT_TOKEN и т.д.)
load_dotenv()

# Уровень логов: INFO — видим основные события
logging.basicConfig(level=logging.INFO)

# Создаём объекты бота и диспетчера (диспетчер раздаёт сообщения обработчикам)
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    """Обработчик команды /start — бот приветствует пользователя."""
    await message.answer(
        "Привет! Я эхо-бот.\n"
        "Напиши что угодно — и я повторю это тебе."
    )


@dp.message()
async def echo_message(message: types.Message) -> None:
    """
    Обработчик любого сообщения — просто отправляем его текст обратно (эхо).
    Если пользователь отправил не текст (фото, стикер и т.д.), пробуем переслать копию.
    """
    if message.text:
        # Обычный текст — отвечаем тем же текстом
        await message.answer(message.text)
    else:
        # Картинка, стикер и т.д. — пробуем отправить копию сообщения
        try:
            await message.send_copy(chat_id=message.chat.id)
        except TypeError:
            await message.answer("Я умею повторять только текст. Напиши текстом :)")


async def main() -> None:
    """Запуск бота: удаляем вебхук (если был) и начинаем опрос сервера Telegram (polling)."""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
