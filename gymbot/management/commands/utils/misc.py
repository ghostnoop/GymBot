import aiogram
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from django.conf import settings


bot = aiogram.Bot(settings.TOKEN)
bot.parse_mode = "HTML"
dp = aiogram.dispatcher.Dispatcher(bot, storage=MemoryStorage())
