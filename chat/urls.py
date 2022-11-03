from django.urls import path

from chat.views import RoomListView, ChatView

urlpatterns = [
    path(r'', RoomListView.as_view(), name='rooms_list'),
    path(r'chat/<int:pk>/', ChatView.as_view(), name='chat'),
]
