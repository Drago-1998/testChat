from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from chat.models import Message


def send_message_ws(message: Message):
    """
    Send massage to WebSocket
    :param message:
    :return:
    """
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        str('chat_' + message.room.name),
        {
            'type': 'chat_message',
            'message': message.text,
            'user_id': message.user_id,
            'username': message.user.username,
            'uuid': message.uuid,
            'created': message.created_at.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        }
    )
