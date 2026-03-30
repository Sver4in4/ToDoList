import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import json

TOKEN = "ТВОЙ_ТОКЕН_ОТ_BOTFATHER"
bot = Bot(token=TOKEN)
dp = Dispatcher()


# 1. Кнопка для запуска Mini App
@dp.message(Command("start"))
async def start(message: types.Message):
    markup = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(
            text="Открыть Todo",
            web_app=types.WebAppInfo(url="https://твой-сайт.рф/index.html")  # Сюда вставь ссылку на свой сайт
        )]],
        resize_keyboard=True
    )
    await message.answer("Жми кнопку, чтобы управлять задачами!", reply_markup=markup)


# 2. Логика приема задачи и "пинга" (уведомлений)
async def persistent_ping(chat_id, task_text):
    for i in range(3):  # Отправит 3 сообщения подряд
        await bot.send_message(chat_id, f"🔔 НАПОМИНАНИЕ: {task_text}")
        await asyncio.sleep(10)  # Интервал 10 секунд (для теста)


@dp.message(lambda message: message.web_app_data)
async def handle_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    task_name = data.get("task")

    await message.answer(f"✅ Задача '{task_name}' принята! Пингану через минуту.")

    # В реальности тут нужна логика планировщика (например, asyncio.sleep до нужного времени)
    asyncio.create_task(persistent_ping(message.chat.id, task_name))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
