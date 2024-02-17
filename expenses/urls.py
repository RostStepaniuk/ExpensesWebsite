from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    #Этот путь соответствует корневому URL, и он связан с функцией views.index. 
    # Когда пользователь попадает на корневой URL, вызывается функция index из модуля views. 
    # Название name="expenses" используется для идентификации этого маршрута в шаблонах.
    path('', views.index, name="expenses"),
    path('add-expense', views.add_expense, name="add-expenses"),
    #этот путь обрабатывает запросы по URL-адресу "/expense-delete/1/", 
    # где <int:id> - идентификатор записи для удаления.
    path('edit-expense/<int:id>', views.expense_edit, name="expense-edit"),
    path('expense-delete/<int:id>', views.delete_expense, name="expense-delete"),
    # вызывает функцию search_expenses из модуля views, 
    # но сначала оборачивает ее в декоратор csrf_exempt
    path('search-expenses', csrf_exempt(views.search_expenses),
         name="search_expenses"),
    path('expense_category_summary', views.expense_category_summary,
         name="expense_category_summary"),
    path('stats', views.stats_view,
         name="stats"),
     path('get_expenses', views.get_expenses, name='get_expenses'),
]
