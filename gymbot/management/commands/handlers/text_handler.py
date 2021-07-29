from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from django.db.models import QuerySet

from gymbot.management.commands.services.sendler import bot_send_message
from gymbot.management.commands.utils.misc import bot
from gymbot.models import *


async def message_handler(message: Message, state: FSMContext):
    print(message)
    subscriber, created = Subscriber.objects.get_or_create(id=message.from_user.id)
    if message.from_user.username is not None:
        subscriber.username = message.from_user.username
        subscriber.save()

    history: QuerySet = MessageHistory.objects.filter(answered=False, for_user_id=message.from_user.id)
    if history.exists():
        history: MessageHistory = history.last()
        history.answered = True
        history.answer_message_id = message.message_id

        history.save()
        if history.message is not None:
            obj, createdq = SubscriberMessage.objects.get_or_create(message=history.message, subscriber=subscriber,
                                                                    defaults={
                                                                        'answer': message.text
                                                                    })

            answer_messages = BotAnswerMessage.objects.filter(for_message=history.message)
            for answer in answer_messages:
                answer: BotAnswerMessage
                text = answer.text
                if text.__contains__('{}'):
                    text = text.format(message.text)

                await bot_send_message(bot, subscriber, text)


async def start_handler(message: Message, state: FSMContext):
    bot_message = BotMessage.objects.get(day=-1)
    print(message.from_user)
    subscriber, created = Subscriber.objects.get_or_create(id=message.from_user.id)
    if message.from_user.username is not None:
        subscriber.username = message.from_user.username
        subscriber.save()
    await bot_send_message(bot, subscriber, bot_message.text)
