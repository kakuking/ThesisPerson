from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async

import json
from datetime import datetime
import pytz

import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .models import Light, TelegramUser
from .serializers import LightSerializer, TelegramUserSerializer

lightGroup = "lightGroup"
telegramUserGroup = "UserGroup"

class LightConsumer(AsyncWebsocketConsumer):
    # lightGroup = "my_group"
    async def connect(self):
        # Accept the WebSocket connection and add to layer group
        await self.accept()
        await self.channel_layer.group_add(lightGroup, self.channel_name)
        

    async def disconnect(self, close_code):
        # Perform reomve from layer group
        await self.channel_layer.group_discard(lightGroup, self.channel_name)
        pass
    
    @database_sync_to_async  # a method that goes in your TestConsumer class
    def update_key_query(self):
        li = Light()
        li.save()
    
    @database_sync_to_async
    def getLight(self, pk):
        li = Light.objects.get(pk=pk)
        ser = LightSerializer(li)
        return ser.data

    @database_sync_to_async
    def getAllLight(self):
        li = Light.objects.all()
        ser = LightSerializer(li, many=True)
        return ser.data


    async def receive(self, text_data):
        # Handle incoming messages
        await self.update_key_query()
        pass

    async def send_message(self, message):
        await self.send(json.dumps(message))

class UserConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        # Accept the WebSocket connection and add to layer group
        await self.accept()
        await self.channel_layer.group_add(telegramUserGroup, self.channel_name)
        

    async def disconnect(self, close_code):
        # Perform reomve from layer group
        await self.channel_layer.group_discard(telegramUserGroup, self.channel_name)
        pass

    async def receive(self, text_data):
        # Handle incoming messages
        # await self.update_key_query()
        pass

    async def send_message(self, message):
        await self.send(json.dumps(message))

@receiver(post_save, sender=Light)
def LightPostSave(sender, instance, update_fields, created, **kwargs):
    # print('\na light has been changed!')
    # print(instance.registeredUsers.all())
    # print(instance.isOn)
    # print(instance.id)

    ser = LightSerializer(instance)

    #send to website
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        lightGroup,
        {"type": "send_message", "message": ser.data}
    )
    
    #send a telegram message and changes nmumber of oks
    if(update_fields):
        if 'isOn' in update_fields and instance.isOn == True and not created:
            for us in instance.registeredUsers.all():
                instance.numberOfOkays -= 1
                telegramNotifMessage(us, instance.id)
            instance.save()
        # if 'numberOfOkays' in update_fields:


@receiver(m2m_changed, sender=Light.registeredUsers.through)
def UsersM2MChange(sender, instance, action, pk_set, **kwargs):
    # print('\na user has been changed!')
    # print(instance.registeredUsers.all())
    # print(instance.isOn)
    if (action=='post_add' or action == 'post_remove'):
        for pk in pk_set:
            user = TelegramUser.objects.get(pk=pk)
            ser = TelegramUserSerializer(user)
            li =  user.light_set.all()
            dat = ser.data
            dat['Lights'] = []
            for l in li:
                dat['Lights'].append(l.id)
            # print(dat['Lights'])
            #send to website
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                telegramUserGroup,
                {"type": "send_message", "message": dat}
            )
    

def telegramNotifMessage(user, lightID):
    # print(f"{user.notificationStartTime} + {datetime.now(tz=pytz.timezone('CET')).time()} + {user.notificationEndTime}")
    if (user.notificationStartTime <= datetime.now(tz=pytz.timezone('CET')).time() <= user.notificationEndTime):
        bot_token = '5915070249:AAHlS7DlWv7c7QGco08Gr_S9NB1kRWbkqkA'    
        bot = telegram.Bot(token=bot_token)
        stopItButton = InlineKeyboardButton('Stop the notification', callback_data='stopNotfication')
        callPoliceButton = InlineKeyboardButton('Call the police', callback_data='callPolice')
        keyboard = [[stopItButton, callPoliceButton]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        bot.send_message(chat_id=user.telegramChatID, text=f'Your registered light, Light {lightID} was triggered between your specified times :', reply_markup=reply_markup)
