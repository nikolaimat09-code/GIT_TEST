"""
Заглушка телеграм-бота на aiogram 3.
Токен берётся из переменной BOT_TOKEN в .env.
Запуск: python bot.py
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
    await message.answer("Привет! Я заглушка бота. Здесь будет твоя логика.")


@dp.message()
async def any_message(message: types.Message) -> None:
    """Обработчик любого другого сообщения (пока просто эхо)."""
    await message.answer("Пока я только заглушка. Добавь свои команды и обработчики.")


async def main() -> None:
    """Запуск бота: удаляем вебхук (если был) и начинаем опрос сервера Telegram (polling)."""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
