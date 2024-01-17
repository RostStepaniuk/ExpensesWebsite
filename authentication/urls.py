from .views import RegistrationView, UsernameValidationView, EmailValidationView, LogoutView, VerificationView, LoginView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


#В Django используется два основных подхода для написания представлений (views): 
#функциональные представления и классы представлений (class-based views, CBVs).
#Для классов представлений используется метод .as_view(), чтобы преобразовать класс в функцию, 
#  которую может понять URL-диспетчер
urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    #csrf_exempt запросы к этому URL-адресу освобождаются от проверки CSRF-токена 
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()),
         name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()),
         name='validate_email'),
     #<token> Этот токен — это безопасный случайно сгенерированный токен, 
     #  который связан с конкретным пользователем.
     #<uidb64>: Это Base64-кодированный идентификатор пользователя.
     #id юзера кодируется, чтобы скрыть его реальное значение и сделать ссылку безопаснее.
    path('activate/<uidb64>/<token>',
         VerificationView.as_view(), name='activate'),
]
