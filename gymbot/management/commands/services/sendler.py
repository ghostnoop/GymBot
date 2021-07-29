import asyncio
from datetime import datetime, timedelta, date

from aiogram import Bot
from aiogram.utils.exceptions import BotBlocked, RetryAfter
from django.db.models import QuerySet
from django.utils import timezone

from gymbot.models import *


async def send_messages(bot: Bot):
    now = datetime.now()
    today = now.date()

    print(today, now)
    for i in range(0, 7):
        day = i + 1
        # day = i
        try:
            bot_message: BotMessage = BotMessage.objects.get(time_during_the_day__hour=now.hour, day=day)

            subscribers = Subscriber.objects.filter(created_at=(today - timedelta(days=day)), alive=True)
            print(len(subscribers), 'subs')

            text = bot_message.text

            for subscriber in subscribers:
                subscriber: Subscriber
                await bot_send_message(bot, subscriber, text, bot_message)
        except Exception as e:
            # print(e)
            pass
        if int(now.hour) == 13:
            try:
                msgs = MessageHistory.objects.exclude(message=None).filter(message__day=day, answered=False)
                for msg in msgs:
                    msg: MessageHistory
                    answer = BotAnswerMessage.objects.get(for_message=msg.message)
                    try:
                        sub = Subscriber.objects.get(id=msg.for_user_id)
                        if sub.created_at == (today - timedelta(days=day)):
                            await bot_send_message(bot, sub, answer.text)
                    except:
                        pass

            except:
                pass


async def bot_send_message(bot: Bot, subscriber, text, bot_message=None):
    try:
        message_id = await bot.send_message(subscriber.id, text)
        MessageHistory.objects.create(for_user_id=subscriber.id,
                                      message=bot_message,
                                      tg_message_id=message_id)
        return True

    except BotBlocked as e:
        subscriber.alive = False
        subscriber.save()
        return False

    except RetryAfter as e:
        print(f"Target [ID:{subscriber.id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout + 1)
        message_id = await bot.send_message(subscriber.id, text)
        MessageHistory.objects.create(for_user_id=subscriber.id,
                                      message=bot_message,
                                      tg_message_id=message_id)
        return True

    except Exception as e:
        print(e)
        return False
