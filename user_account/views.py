from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from userpreferences.models import UserPreference
from django.contrib.auth.models import User


@login_required(login_url='/authentication/login')
def index(request):
    user = request.user
    try:
        # Assuming you have a OneToOne relationship between User and UserPreference
        currency = UserPreference.objects.get(user=user).currency
    except UserPreference.DoesNotExist:
        currency = 'Default Currency'  # Replace with your default currency

    context = {
        'username': user.username,
        'email': user.email,
        'currency': currency,
    }
    return render(request, 'user_account/user_account.html', context)



