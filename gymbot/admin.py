from django.contrib import admin

# Register your models here.
from gymbot.models import Subscriber, SubscriberMessage, BotMessage, BotAnswerMessage, MessageHistory


class BotMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'day', 'time_during_the_day', 'text')
    search_fields = ('id', 'day')
    list_filter = ('day', 'time_during_the_day')


admin.site.register(BotMessage, BotMessageAdmin)


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'alive', 'username')
    search_fields = ('id', 'created_at')
    list_filter = ('alive',)


admin.site.register(Subscriber, SubscriberAdmin)


class SubscriberMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'subscriber', 'message', 'answer')
    search_fields = ('id', 'subscriber', 'message')


admin.site.register(SubscriberMessage, SubscriberMessageAdmin)


class BotAnswerMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'for_message', 'text')


admin.site.register(BotAnswerMessage, BotAnswerMessageAdmin)


class HistoryMessageAdmin(admin.ModelAdmin):
    list_display = ('for_user_id', 'message', 'tg_message_id', 'answered', 'answer_message_id')


admin.site.register(MessageHistory, HistoryMessageAdmin)
