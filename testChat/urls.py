from django.contrib import admin
from django.urls import path, include

from chat.router import router as chat_router
from testChat.router import main_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("chat.urls")),
    path("api/v1/", include(main_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
