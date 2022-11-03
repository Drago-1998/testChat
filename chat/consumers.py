import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# Rooms global data
rooms = {}


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        if rooms.get(self.room_name):
            rooms[self.room_name]['users_count'] += 1
        else:
            rooms[self.room_name] = {
                'users_count': 1
            }


        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

        # Send massage all chat users notification
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "users_count_change",
                                   "users_count": rooms[self.room_name]['users_count']}
        )

    def disconnect(self, close_code):

        # Leave room group
        if rooms[self.room_name]['users_count'] == 1:
            del rooms[self.room_name]
        else:
            rooms[self.room_name]['users_count'] -= 1

        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

        # Send massage all chat users notification
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "users_count_change",
                                   "users_count": rooms[self.room_name]['users_count']}
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        user_id = event["user_id"]
        uuid = event["uuid"]
        created = event["created"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            "type": 'chat_massage',
            "message": message,
            "user_id": user_id,
            "username": username,
            "uuid": uuid,
            "created": created
        }))

    # Receive message from room group
    def users_count_change(self, event):
        users_count = event["users_count"]

        # Send notification to WebSocket
        self.send(text_data=json.dumps({
            "type": 'notification',
            "users_count": users_count,
        }))
