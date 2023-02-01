from django.contrib import admin
from django.urls import path, re_path

from Dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('lights/', views.LightGetAll),
    path('lights/create/', views.LightCreate),
    path('lights/<int:pk>/', views.LightGet),
    path('lights/<int:pk>/updateIsOn/', views.LightUpdateIsOn),
    path('lights/<int:pk>/delete/', views.LightDelete),
    path('lights/getIndexRange', views.getLightIndexRange),
    path('lights/<int:pk>/isOk', views.incLightIsOK),

    path('user/registerLights', views.registerLights),
    path('user/deregisterLights', views.deregisterLights),
    path('user/<int:pk>/getLights', views.getUserLights),
    path('user/<int:pk>/getTimes', views.getUserTimes),
    path('user/setStartTIme', views.setStartTime),
    path('user/setEndTime', views.setEndTime),

    path('TelegramUsers/', views.usersPage),

    path('TestAWS/', views.confirm_url_AWS),
    path('TestAWS/message/', views.AWSTrial),
]
