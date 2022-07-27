import logging
import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from aiogram import Bot, types

from aiogram.dispatcher.filters import Text


TOKEN = os.getenv('BOT_TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()

@dp.message_handler(Text(equals="Добавить \U00002795\U0001FAB4"))
async def with_puree(message: types.Message):
    await message.reply("Выбери из списка")

@dp.message_handler(Text(equals="Создать вручную \U0000270F\U0001FAB4"))
async def with_puree(message: types.Message):
    await message.reply("Название/время")

@dp.message_handler(Text(equals="Создать вручную \U0000270F\U0001FAB4"))
async def with_puree(message: types.Message):
    await message.reply("Выбери из списка")

@dp.message_handler(Text(equals="Удалить \U0000274C\U0001FAB4"))
async def with_puree(message: types.Message):
    await message.reply(":(")

@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons1 = ["Добавить \U00002795\U0001FAB4", "Создать вручную \U0000270F\U0001FAB4"]
    buttons2 = ["Информация \U0001F4D6\U0001FAB4", "Удалить \U0000274C\U0001FAB4"]
    keyboard.add(*buttons1)
    keyboard.add(*buttons2)
    await message.answer("Привет, я помогу твоим цветочкам не зачахнуть. Добавь цветок и я буду напоминать тебе о том когда его нужно полить", reply_markup=keyboard)

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )