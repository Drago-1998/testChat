from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, TemplateView, CreateView, DetailView

from chat.models import Room


class RoomListView(ListView):
    queryset = Room.objects.filter(active=True)
    template_name = 'chat/room_list.html'
    context_object_name = 'rooms'

    def post(self, request):
        """
        Create room object
        :param request:
        :return:
        """
        room = Room.objects.create(name=request.POST.get('room_name'))
        return redirect(reverse('chat', kwargs={'pk': room.id}))


class ChatView(DetailView):
    model = Room
    template_name = 'chat/chat.html'
    context_object_name = 'room'
