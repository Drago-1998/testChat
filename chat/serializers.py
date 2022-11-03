from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from chat.helper import send_message_ws
from chat.models import Message


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = 'id', 'username'


class MessageSerializer(ModelSerializer):
    user_obj = UserSerializer(many=False, read_only=True, source='user')

    def create(self, validated_data):
        message = super(MessageSerializer, self).create(validated_data)
        send_message_ws(message)
        return message

    class Meta:
        model = Message
        fields = 'id', 'created_at', 'updated_at', 'text', 'user_obj', 'user', 'room', 'uuid'
