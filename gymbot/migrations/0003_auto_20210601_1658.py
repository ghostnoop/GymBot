# Generated by Django 3.1.6 on 2021-06-01 13:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gymbot', '0002_messagehistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagehistory',
            name='answer_message_id',
            field=models.BigIntegerField(default=None, null=True),
        ),
    ]
