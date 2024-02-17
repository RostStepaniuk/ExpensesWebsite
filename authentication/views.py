from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth

# Create your views here.

#класс проверяет доступность и правильность емеила при регистрации
class EmailValidationView(View):
    def post(self, request):
        #принимает запрос с данними и превращает их в json,
        # затем доастает оттуда поле email
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})

#класс проверяет правильность введенного никнейма
class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        #.isalnum() - возвращает True, если строка состоит только из букв и/или цифр
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})


#регистрация пользователей
class RegistrationView(View):
    #GET-запрос, отображает страницу регистрации.
    def get(self, request):
        return render(request, 'authentication/register.html')
    #заполнения формы регистрации и её отправки пользователем.
    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # create a user account
        #**************************************************************************
        #сначала извлекаются данные, отправленные пользователем
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }
        #проверка на наличия юзера с таким логином и меилом
        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                #проверка длини пароля
                if len(password) < 6:
                    #message. передается в html шаблон 
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                try:
                    user = User.objects.create_user(username=username, email=email)
                    user.set_password(password)
                    user.is_active = False
                    user.save()
                    #get_current_site используется чтобы использовать доменное имя и 
                    #  включить его в ссылку для активации аккаунта в вашем письме.
                    current_site = get_current_site(request)
                    email_body = {
                        'user': user,
                        'domain': current_site.domain,
                        #кодирует user.pk в бити и base64 кодировку
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
    #----------------------------------------------------------------------------------------
                        #создается токен
                        'token': account_activation_token.make_token(user),
                    }
                    #revers позволяет получить URL-адрес для заданного имени маршрута "activate"
                    link = reverse('activate', kwargs={
                        'uidb64': email_body['uid'], 'token': email_body['token']})
                        #kwargs является сокращением от "keyword arguments" 
                        #специальный тип аргумента в функциях и методах, который позволяет передавать аргументы в виде словаря с ключами и значениями.
                                

                    email_subject = 'Activate your account'

                    activate_url = 'http://'+current_site.domain+link
                    #сообщение на меиле которое прийдет пользователю для подтверждения регитсрации
                    email = EmailMessage(
                        email_subject,
                        '\n\nHi '+user.username + ', \nPlease follow the link below to activate your account \n\n'+activate_url,
                        'noreply@semycolon.com',
                        [email],
                    )
                    email.send(fail_silently=False)
                    messages.success(request, 'Account is almost created!\nCheck your email and confirm registration.')
                except Exception as e:
                    messages.error(request, 'Something went wrong...')
                return render(request, 'authentication/login.html', context)
        #избиточний код
        messages.error(request, 'Something went wrong...')
        return render(request, 'authentication/register.html', context)


#класс обрабативает активацию учетних записей
class VerificationView(View):
    #метод ожидает два параметра в URL: uidb64 и token, 
    # которые используются для проверки и активации
    def get(self, request, uidb64, token):
        try:
            #извлекаем id из закодировонного idb64
            id = force_str(urlsafe_base64_decode(uidb64))
            #получаем user на основе извлеченного id
            user = User.objects.get(pk=id)

            #cовпадает ли переданный token с токеном активации учетной записи user
            #если да, продолжаем проверку
            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')
            
            #если уже активирована, перенаправляет на страницу
            if user.is_active:
                return redirect('login')
            
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')

        except Exception as ex:
            pass
        # избиточний код
        # return redirect('login')

#отвечает за логирование
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            #функция выполняет проверку и возвращает объект пользователя, если учетные данные верны.
            user = auth.authenticate(username=username, password=password)
            #если обьект бил возвращен
            if user:
                #если пользовать активирован впускаем в систему 
                #и перенаправляем на страничку расходов
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' +
                                     user.username+' you are now logged in')
                    return redirect('expenses')
                messages.error(
                    request, 'Account is not active,please check your email')
                return render(request, 'authentication/login.html')
            messages.error(
                request, 'Invalid credentials,try again')
            return render(request, 'authentication/login.html')

        messages.error(
            request, 'Please fill all fields')
        return render(request, 'authentication/login.html')

#класс вихода из аккаунта
class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')
