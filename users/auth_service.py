from rest_framework import authentication
from rest_framework.validators import ValidationError
from users.models import CustomUser
from string import printable
from random import choice


class Authentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'SMS_code'

    def authenticate(self, request, sms_code=None, **kwargs):
        auth_header = authentication.get_authorization_header(request).split()
        if not auth_header:
            return None

        if all([len(auth_header) < 1, len(auth_header) > 2]):
            raise ValidationError('Неверно передан код авторизации')

        return self.authenticate_credentials(str(auth_header[1]))

    def authenticate_credentials(self, user_input):
        try:
            user = CustomUser.objects.get(auth_code=user_input[2:6])
        except KeyError:
            raise ValidationError('Неверный код авторизации')
        except CustomUser.DoesNotExist:
            raise ValidationError('Неверно передан код авторизации')

        if user.invite_code is None:
            user.invite_code = ''.join([choice(printable.replace(printable[-15], '')[:-6]) for _ in range(6)])
            user.save()
        if not user.is_active:
            user.is_active = True
            user.save()

        return user, None
