import json
from datetime import time

from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from .serializers import LightSerializer
from .models import Light, TelegramUser

# Create your views here.
def index(request):
    lights = Light.objects.all()
    return render(request, 'Dashboard/index.html', { 'Lights': lights })

def usersPage(request):
    telegramUsers = TelegramUser.objects.all()
    return render(request, 'Dashboard/telegramUsers.html', { 'TelegramUsers': telegramUsers })


#####                                                           API STUFF BELOW - CAUTION

@csrf_exempt
def AWSTrial(request):
    print("yoyooyyoyo")
    print(request.body)

    return HttpResponse(status=201)

@csrf_exempt
def AWSUpdate(request):
    data = request.POST
    print(data)
    lightID = data['lightID']
    isOn = False if data['isOn'] == 'False' else True
    print(f"{lightID} and {isOn} ")

    li = Light.objects.get(pk = lightID)
    li.isOn = isOn
    li.save()
    print(li)
    # light.save(update_fields=['isOn'])
    
    # Return the headers and payload as the response
    return HttpResponse(status=200)

@csrf_exempt
def updateOverride(request):
    data = request.body
    print(data)
    print("updateOveride")

    return HttpResponse(status=200)


#LIght indices
def getLightIndexRange(request):
    if request.method == 'GET':
        di = {
            'min': Light.objects.first().id,
            'max': Light.objects.last().id
            }
        return JsonResponse(di, status=201)

#Check if user exists, then put him in the light they sent
@csrf_exempt
def registerLights(request):
    data = request.POST
    # print(data.getlist('lights'))
    userID = data['userID']
    username = data['username']
    chatID = data['chatID']
    lights = data.getlist('lights')
    
    try:
        tUser = TelegramUser.objects.get(telegramUserID= data['userID'])
    except TelegramUser.DoesNotExist:
        tUser = TelegramUser(telegramChatID=chatID, telegramUserID=userID, telegramUsername=username)
        tUser.save()

    for light in lights:
        li = Light.objects.get(pk=light)
        li.registeredUsers.add(tUser)
        li.save()

    return HttpResponse(status=201)

@csrf_exempt
def deregisterLights(request):
    data = request.POST
    userID = data['userID']
    lights = data.getlist('lights')
    
    for light in lights:
        li = Light.objects.get(pk=light)
        tUser = TelegramUser.objects.get(telegramUserID=userID)
        li.registeredUsers.remove(tUser)
        li.save()

    return HttpResponse(status=201)


@csrf_exempt
def setStartTime(request):
    data = request.POST
    userID = data['userID']
    tim = data.getlist('time')
    user = TelegramUser.objects.get(telegramUserID=userID)
    ti = time(int(tim[0]), int(tim[1]), int(tim[2]))
    user.notificationStartTime = ti
    user.save()
    return HttpResponse(status=201)

@csrf_exempt
def setEndTime(request):
    data = request.POST
    userID = data['userID']
    tim = data.getlist('time')
    user = TelegramUser.objects.get(telegramUserID=userID)
    ti = time(int(tim[0]), int(tim[1]), int(tim[2]))
    user.notificationEndTime = ti
    user.save()
    return HttpResponse(status=201)

@csrf_exempt
def getUserLights(request, pk):
    if request.method == 'GET':
        us = TelegramUser.objects.get(telegramChatID=pk)
        userLights = us.light_set.all()
        lights = []
        for li in userLights:
            lights.append(li.id)
        return JsonResponse(lights, safe=False, status = 201)
    
@csrf_exempt
def getUserTimes(request, pk):
    if request.method == 'GET':
        us = TelegramUser.objects.get(telegramChatID=pk)
        dic = {
            "startTime": us.notificationStartTime,
            "endTime": us.notificationEndTime
        }
        return JsonResponse(dic, status=201)


#CRUD stuff
@csrf_exempt
def LightCreate(request):
    if request.method == 'POST':
        # data = await rqe
        serializer = LightSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def LightGetAll(request):
    if request.method == 'GET':
        lights = Light.objects.all()
        serializer = LightSerializer(lights, many = True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def LightGet(request, pk):
    if request.method == 'GET':
        light = Light.objects.get(pk=pk)
        serializer = LightSerializer(light)
        return JsonResponse(serializer.data)
    
@csrf_exempt
def LightUpdateIsOn(request, pk):
    if request.method == 'POST':
        light = get_object_or_404(Light, pk=pk)
        isOn = False if request.POST['isOn'] == 'False' else True
        light.isOn = isOn
        light.save(update_fields=['isOn'])
        return HttpResponse(status=201)

@csrf_exempt
def incLightIsOK(request, pk):
    if request.method == 'POST':
        light = get_object_or_404(Light, pk=pk)
        light.numberOfOkays += 1
        light.save(update_fields=['numberOfOkays'])
        return HttpResponse(status=201)

@csrf_exempt
def LightDelete(request, pk):
    if request.method == 'DELETE':
        light = get_object_or_404(Light, pk=pk)
        light.delete()
        return HttpResponse(status=204)