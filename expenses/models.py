from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here. 

#модель, представляющая таблицу расходов
class Expense(models.Model):
    #(сумма расхода)
    amount = models.FloatField()
    #дата расхода
    date = models.DateField(default=now)
    description = models.TextField()
    #владелец расхода, связанный с моделью User через внешний ключ
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=266)

    #отображает текст обьекта модели Expense(имя категории в данном случае)
    #например при визове print(expense) ми увидим "название категории"
    def __str__(self):
        return self.category

    #ordering используется для определения порядка сортировки записей 
    #-date указывает, что записи будут сортироваться по убыванию
    class Meta:
        ordering: ['-date']

#модель, представляющая таблицу категорий.
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
