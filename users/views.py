from rest_framework.response import Response
from users.serializers import CustomUserSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from users.models import CustomUser
from random import choice
from string import printable
from time import sleep
from users.permissions import IsProfileOwner


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = request.data['password']
        user = CustomUser.objects.get(pk=serializer.data['id'])
        user.set_password(password)
        user.is_active = False
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def put(self, request, *args, **kwargs):

        if request.data.get('invite_code'):
            try:
                if request.data.get('invite_code'):
                    user = CustomUser.objects.get(invite_code=request.user.invite_code)
            except CustomUser.DoesNotExist:
                raise ValidationError('Пользователя с таким инвайт кодом не существует')
            except KeyError:
                raise ValidationError('Запрос составлен неверно')

        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):

        if request.data.get('invite_code'):
            try:
                user = CustomUser.objects.get(invite_code=request.user.invite_code)
            except CustomUser.DoesNotExist:
                raise ValidationError('Пользователя с таким инвайт кодом не существует')
            except KeyError:
                raise ValidationError('Запрос составлен неверно')

        return self.partial_update(request, *args, **kwargs)


class UserProfileAPIView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)


class SMSCodeView(generics.GenericAPIView):

    def post(self, request):

        try:
            user = CustomUser.objects.get(phone_number=request.data['phone_number'])
            authorization_code = ''.join([choice(printable.replace(printable[-15], '')[:-6]) for _ in range(4)])
            sleep(1)
            print(authorization_code)
            user.auth_code = authorization_code
            user.save()

            return Response(status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            raise ValidationError('Пользователя с таким номером не существует')
        except KeyError:
            raise ValidationError('Номер телефона передан неверно')
