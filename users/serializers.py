from rest_framework.serializers import ModelSerializer, SerializerMethodField
from users.models import CustomUser


class CustomUserSerializer(ModelSerializer):

    invited_users = SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'phone_number', 'city', 'invite_code', 'invited_users')

    def get_invited_users(self, instance):
        return [user.phone_number for user in CustomUser.objects.filter(invite_code=instance.invite_code)]
