from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger





#поиск доходов
def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        #.values() в Django используется для извлечения значений полей из объектов модели 
        # (или QuerySet) и представления их в виде словарей
        data = income.values()
        return JsonResponse(list(data), safe=False)


#єто метод отвечающий за отображение страници с доходами
#показивает доходи юзера, обьект страници и валюту
@login_required(login_url='/authentication/login')
def index(request):
    categories = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'income/index.html', context)


#добавление дохода
@login_required(login_url='/authentication/login')
def add_income(request):
    sources = Source.objects.all()
    #контекст содержит имена источников а так же пост.запрос отправленний юезром
    context = {
        'sources': sources,
        'values': request.POST
    }
 
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        new_source = request.POST.get('new_source')
        if new_source:
            # Create a new Source object if a new source was provided
            source_obj, created = Source.objects.get_or_create(name=new_source)
            source = source_obj.name  # Use the name of the new or existing source
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        
        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/add_income.html', context)

        UserIncome.objects.create(owner=request.user, amount=amount, date=date,
                                  source=source, description=description)
        messages.success(request, 'Record saved successfully')

        return redirect('income')


#редактирование дохода
@login_required(login_url='/authentication/login')
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'income/edit_income.html', context)
        income.amount = amount
        income. date = date
        income.source = source
        income.description = description

        income.save()
        messages.success(request, 'Record updated  successfully')

        return redirect('income')


def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'record removed')
    return redirect('income')

# предназначен для получения сводной информации о доходах в разных 
# категориях за последние 6 месяцев
def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)
    incomes = UserIncome.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}
    
    def get_source(expense):
        return expense.source
    source_list = list(set(map(get_source, incomes)))

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)
        
        for item in filtered_by_source:
            amount += item.amount
        return amount
    
    for source in source_list:
        finalrep[source] = get_income_source_amount(source)

    return JsonResponse({'income_source_data': finalrep}, safe=False)
    


def stats_view(request):
    return render(request, 'income/stats.html')



def get_incomes(request):
    page = request.GET.get('page', 1)
    per_page = 4  # Number of items per page

    incomes = UserIncome.objects.filter(owner=request.user).order_by('-date')
    paginator = Paginator(incomes, per_page)
    
    try:
        incomes = paginator.page(page)
    except PageNotAnInteger:
        incomes = paginator.page(1)
    except EmptyPage:
        incomes = paginator.page(paginator.num_pages)
    
    income_data = list(incomes.object_list.values('source', 'description', 'amount', 'date'))
    
    return JsonResponse({
        'data': income_data,
        'num_pages': paginator.num_pages,
        'current_page': int(page)
    })

