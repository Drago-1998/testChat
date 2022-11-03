from django.contrib import admin

from chat.models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'created_at', 'active'
    list_filter = ('active', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = 'id', 'text', 'user', 'room', 'created_at'
    list_filter = 'room__name', 'user'
