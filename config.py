import logging
import boto3
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


with open('messages.json', 'r', encoding="utf8") as f:
    messages_text = json.load(f)
with open('users.json', 'r', encoding="utf8") as f:
    users = json.load(f)
API_TOKEN = ''
admins, members = users["admins"], users["members"]
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())


async def send_file():
    pass


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

