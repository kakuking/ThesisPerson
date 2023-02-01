# Generated by Django 4.1.5 on 2023-01-10 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegramChatID', models.IntegerField()),
                ('telegramUserID', models.IntegerField()),
                ('telegramUsername', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='light',
            name='registeredUsers',
            field=models.ManyToManyField(to='Dashboard.telegramuser'),
        ),
    ]
