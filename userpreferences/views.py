from django.shortcuts import render
import os
import json
from django.conf import settings
from .models import UserPreference
from django.contrib import messages
# Create your views here.

#позволяет пользователям выбирать предпочтительную валюту и сохранять её в своем профиле
def index(request):
    currency_data = []
    #путь к файлу с доступними валютами
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    #откриваем файл для чтения ('r').содержимое джсон загружаем в переменную data 
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        #загружаем в список "currency_data"словарь с именем и значением валют
        for k, v in data.items():
            currency_data.append({'name': k, 'value': v})

    exists = UserPreference.objects.filter(user=request.user).exists()
    user_preferences = None
    if exists:
        #если UserPreference существуют для єтого пользователя-инициализируем значение в переменную user_preference
        user_preferences = UserPreference.objects.get(user=request.user)
    if request.method == 'GET':
        #виводим отображения всего списка доступних валют из "currency_data"
        #и валюту юзера из "user_preferences"
        return render(request, 'preferences/index.html', {'currencies': currency_data,
                                                          'user_preferences': user_preferences})
    else:
        #если запрос пост, получаем вибранную валюту
        currency = request.POST['currency']
        #и если она уже существует, заменяем
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            #иначе создается новый объект UserPreference для текущего пользователя с выбранной валютой
            UserPreference.objects.create(user=request.user, currency=currency)
        messages.success(request, 'Changes saved')
        #отображаем шаблон preferences/index.html
        return render(request, 'preferences/index.html', {'currencies': currency_data, 'user_preferences': user_preferences})
    #передавая в контекст данные о доступных валютах currency_data и обновленные предпочтения пользователя user_preferences.



