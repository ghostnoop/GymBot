from django.db import models


class BotMessage(models.Model):
    day = models.IntegerField()
    time_during_the_day = models.TimeField()
    text = models.TextField()

    def __str__(self):
        return f"{self.day} - {self.time_during_the_day} - {self.text[:10]}"

    class Meta:
        db_table = 'bot_message'


class BotAnswerMessage(models.Model):
    for_message = models.ForeignKey(BotMessage, on_delete=models.SET_NULL, null=True)
    text = models.TextField()


class Subscriber(models.Model):
    id = models.BigIntegerField(primary_key=True, unique=True)
    created_at = models.DateField(auto_now_add=True)
    alive = models.BooleanField(default=True)
    username = models.CharField(max_length=255, default="")

    def __str__(self):
        return f"{self.id}, {self.created_at}, {self.alive}"

    class Meta:
        db_table = 'bot_subscriber'


class SubscriberMessage(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.SET_NULL, null=True)
    message = models.ForeignKey(BotMessage, on_delete=models.SET_NULL, null=True)
    answer = models.TextField()

    class Meta:
        unique_together = ['subscriber', 'message']
        db_table = 'subscriber_message'


class MessageHistory(models.Model):
    for_user_id = models.BigIntegerField()
    message = models.ForeignKey(BotMessage, on_delete=models.SET_NULL, null=True)
    tg_message_id = models.BigIntegerField()
    answered = models.BooleanField(default=False)
    answer_message_id = models.BigIntegerField(null=True, default=None)

    class Meta:
        unique_together = ['for_user_id', 'tg_message_id']
