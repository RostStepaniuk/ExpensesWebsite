from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

#AppTokenGenerator, используется для создания токенов, которые используются 
#  в приложении для активации учетных записей пользователей (authentication)
class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        #переопределенний метеод генерирующий токен в зависимости от прописанних факторов 
        return (text_type(user.is_active) + text_type(user.pk) + text_type(timestamp))


account_activation_token = AppTokenGenerator()


"""Изначально в Django используется стандартный PasswordResetTokenGenerator, 
который создает токены c учетом только идентификатора пользователя (user.pk) 
и временной метки (timestamp). Однако в вашем случае было решено включить также 
статус активации пользователя (user.is_active) в формирование ключа, чтобы учитывать 
этот статус при проверке токена. """
