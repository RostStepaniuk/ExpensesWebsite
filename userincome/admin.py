from django.contrib import admin
from .models import UserIncome, Source
# Register your models here.

#означает, что модели UserIncome и Source 
# будут доступны в административном интерфейсе Django
admin.site.register(UserIncome)
admin.site.register(Source)