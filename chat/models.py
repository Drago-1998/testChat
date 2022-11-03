from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    """
    Base Abstract Model
    used: Room, Message - models
    """
    created_at = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Изменено', auto_now=True)

    class Meta:
        abstract = True


class Room(BaseModel):
    """
    Room model (Chat) - chat rooms
    """
    name = models.CharField(verbose_name='Название чата', max_length=255)
    active = models.BooleanField(verbose_name='Статус (Активен?)', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(BaseModel):
    """
    Message model - store all messages
    """
    room = models.ForeignKey(Room, verbose_name='Чат', on_delete=models.PROTECT)
    text = models.TextField(verbose_name='Сообщение')
    uuid = models.CharField(verbose_name='UUID', max_length=255)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = 'Сообщения'
        verbose_name = 'Сообщение'
