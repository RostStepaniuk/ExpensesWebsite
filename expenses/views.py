from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
import datetime


# Эта функция обрабатывает поиск расходов. в строке поиска
def search_expenses(request):
    if request.method == 'POST':
        #извлекает из Пост запроса данние в видео джсон с ключoм 'searchText'
        search_str = json.loads(request.body).get('searchText')
        #поиск в БД модели Expense,используя filter()для поиска по условиям
        expenses = Expense.objects.filter(
            #условие, в которих значение amount начинается с текста указанного
            # в поисковой строке 'search_str' c помощью запроса 'istartswith'
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            #тут идет поиск по строчке в любом месте поля description по условию "contains"
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            # '|' оператор или. 
            # owner=request.user ограничение поиска только для текущего юезера
            category__icontains=search_str, owner=request.user)
        #expenses - это QuerySet, представляющий найденные записи
        #values() преобразует этот QuerySet в список словарей
        data = expenses.values()
        #list(data) преобразует список словарей в список списков,
        #safe=False указывает, что это не JSON-сериализуемый объект 
        return JsonResponse(list(data), safe=False)

# Этот метод отображает страницу со списком расходов.
#Представляет декоратор, который ограничивает доступ к представлению 
# только зарегистрированным пользователям.
# иначе перенаправляется на '/authentication/login'
@login_required(login_url='/authentication/login')
def index(request):
    #извлекаются все записи модели Category
    categories = Category.objects.all()
    #извлекает все расходи текущего пользователя. упорядочени по убиванию дати
    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    #разбивает список расходов на страници. на каждой будет по 5 расходов
    paginator = Paginator(expenses, 5)
    #получение номера текущей страници с именем "page"
    page_number = request.GET.get('page')
    # ****************************************
    #получение обьекта страниці для текущей страници для отображения расходов на странице
    page_obj = paginator.get_page(page_number)

    # получаем или создаем пользователя *************
    user_preferences, created = UserPreference.objects.get_or_create(user=request.user)
    #.get_or_create создает кортеж, где первий єелемент  - это объект, который был найден или создан, 
    # и второй элемент - это флаг, который указывает, был ли объект только что создан 
    if created:
        #если пользователь только что создался, по умолчанию устанавливаем $ как валюту
        user_preferences.currency = 'USD'  # Задайте дефолтное значение валюты
        user_preferences.save()
    # # Получаем валюту после get_or_create
    currency = user_preferences.currency  
    # создаем словарь с параметрами 
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    #Отправка данных в шаблон 'expenses/index.html' с использованием функции render.
    return render(request, 'expenses/index.html', context)


# єто метод для создания записях о расходах
@login_required(login_url='/authentication/login')
def add_expense(request):
    # получаем увсе котегории из модели Category
    categories = Category.objects.all()
    # создаем словарь с этими категориями и передаем его в шаблон HTML
    context = {
        'categories': categories,
        'values': request.POST
    }
    # и если єто ГЕТ запрос, передаем его в шаблон HTML
    # Отображаем страницу с формой добавления расхода, 
    # где пользователь может ввести информацию о расходе.
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)
    # если запрос ПОСТ, назначаем переменние amount desc,date, category
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)
        # Создает новую запись о расходе в базе данных с полученными данными 
        # и связывает этот расход с текущим пользователем.
        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        # Выводит сообщение об успешном сохранении расхода.
        messages.success(request, 'Expense saved successfully')
        # Перенаправляет пользователя на страницу, где отображаются все расходы.
        return redirect('expenses')


#метод предоставляет функциональность редактирования существующего расхода.
@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    #идентификатор (id) расхода, который должен быть изменен
    expense = Expense.objects.get(pk=id)
    # список всех катеґорий расходов
    categories = Category.objects.all()
    #список о редактируемом расходе, значениях полей этого расхода и списке категорий.
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    #Если запрос выполняется методом GET (открытие страницы редактирования), 
    # метод возвращает страницу с формой редактирования, заполненной данными о расходе.
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    # запрос выполняется методом POST (отправка формы редактирования)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses')

# метод удаляет расход
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    #перенаправляет пользователя на страницу со списком расходов
    return redirect('expenses')

# предназначен для получения сводной информации о расходах в разных 
# категориях за последние 6 месяцев
def expense_category_summary(request):
    # получаем текущую дату
    todays_date = datetime.date.today()
    #представляет собой дату, находящуюся в прошлом, за 6 месяцев от текущей даты
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    #получаем список всех расходов между сейчас и пол года назад
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}
    #метод возвращает артибут КАТЕГОРИИ каждого расхода
    def get_category(expense):
        #category - єто поле из модели Expanse для хранения категории каждого расхода
        return expense.category
    #список уникальних категорий и set() для исключения повторяющихся категорий.
    #метод map() итерирует каждий елемент списка expenses и передает его в аргумент
    #методу get_category
    category_list = list(set(map(get_category, expenses)))

    #Вычисляет общую сумму расходов в указанной категории.
    def get_expense_category_amount(category):
        amount = 0
        #filtered_by_category -это queryset (набор данных) из объектов Expense, 
        # которые относятся  к конкретной категории
        filtered_by_category = expenses.filter(category=category)
        
        for item in filtered_by_category:
            #item.amount - это доступ к атрибуту amount конкретного объекта Expense 
            # в текущей итерации цикла. Суммируя item.amount на каждой итерации, 
            # мы накапливаем общую сумму расходов в данной категории.
            amount += item.amount
        return amount

    #вычисляем сумму расходов для каждой категории с помощью get_expense_category_amount 
    # и сохраняем эти данные в finalrep
    for category in category_list:
        finalrep[category] = get_expense_category_amount(category)

    return JsonResponse({'expense_category_data': finalrep}, safe=False)
    #ключи этого словаря становятся именами полей JSON-объекта, 
    #  а значения - значениями этих полей.


#отображает страницу статистики, и пользователь видит информацию о расходах.
def stats_view(request):
    return render(request, 'expenses/stats.html')



def get_expenses(request):
    page = request.GET.get('page', 1)
    per_page = 4  # Number of items per page

    expenses = Expense.objects.filter(owner=request.user).order_by('-date')
    paginator = Paginator(expenses, per_page)
    
    try:
        expenses = paginator.page(page)
    except PageNotAnInteger:
        expenses = paginator.page(1)
    except EmptyPage:
        expenses = paginator.page(paginator.num_pages)
    
    income_data = list(expenses.object_list.values('category', 'description', 'amount', 'date'))
    
    return JsonResponse({
        'data': income_data,
        'num_pages': paginator.num_pages,
        'current_page': int(page)
    })