import asyncio
from datetime import datetime

import aiogram
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management import BaseCommand

from gymbot.management.commands import handlers
from gymbot.management.commands.services.sendler import send_messages
from gymbot.management.commands.utils.misc import dp, bot


class Command(BaseCommand):
    help = "Runs consumer."

    def handle(self, *args, **options):
        print("started ")

        bot_start()


def bot_start():
    print('bot running')

    aiogram.executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


async def on_startup(*args, **kwargs):
    handlers.setup(dp)
    await cron_setup(bot)
    print("Bot started")


async def cron_setup(bot: Bot):
    asyncio.create_task(cron_starter(bot, ))


async def cron_starter(bot):
    print('start cron',datetime.now())
    scheduler = AsyncIOScheduler()
    prod = CronTrigger(minute='00')
    test = CronTrigger(minute='41')

    scheduler.add_job(send_messages, trigger=prod, args=(bot,), replace_existing=True)
    scheduler.start()
    # await send_messages(bot)
