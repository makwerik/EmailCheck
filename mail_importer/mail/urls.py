from django.urls import path, include
from .views import EmailAccountViewSet, EmailMessageViewSet, message_list, fetch_emails_view
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'accounts', EmailAccountViewSet)
router.register(r'messages', EmailMessageViewSet)

urlpatterns = [
    path('', message_list, name='message_list'),
    path('api/', include(router.urls)),
    path('api/fetch_emails/', fetch_emails_view, name='fetch_emails'),  # Новый URL для получения писем
]
