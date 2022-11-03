from rest_framework import routers

from chat.api_view import MessageViewSet

router = routers.SimpleRouter()
router.register(r'messages', MessageViewSet)
