from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EventViewSet, 
    TicketViewSet, 
    PostViewSet, 
    NotificationViewSet,
    # RegisterView,  # Раскомментировать при реализации
    # LoginView,     # Раскомментировать при реализации
)

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'posts', PostViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    # Удаляем маршруты для регистрации и входа
    # path('register/', RegisterView.as_view(), name='register'),
    # path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]