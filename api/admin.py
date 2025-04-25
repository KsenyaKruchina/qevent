from django.contrib import admin
from .models import Event, Ticket, Notification, Post


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_date', 'end_date')  # Поля, отображаемые в списке
    search_fields = ('title', 'location')  # Поля, по которым можно искать
    list_filter = ('start_date', 'end_date')  # Фильтры по дате начала и окончания
    ordering = ('start_date',)  # Сортировка по дате начала


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('event', 'is_active', 'is_published', 'purchase_date')  # Поля, отображаемые в списке
    search_fields = ('event__title',)  # Поиск по названию мероприятия
    list_filter = ('is_active', 'is_published')  # Фильтры по статусу активности и публикации
    ordering = ('purchase_date',)  # Сортировка по дате покупки


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'message', 'created_at')  # Поля, отображаемые в списке
    search_fields = ('title', 'message')  # Поиск по заголовку и сообщению
    list_filter = ('created_at',)  # Фильтр по дате создания
    ordering = ('-created_at',)  # Сортировка по дате создания (новые сверху)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'event', 'created_at')  # Поля, отображаемые в списке
    search_fields = ('content', 'event__title')  # Поиск по содержимому и названию мероприятия
    list_filter = ('created_at',)  # Фильтр по дате создания
    ordering = ('-created_at',)  # Сортировка по дате создания (новые сверху)