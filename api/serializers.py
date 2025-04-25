from rest_framework import serializers
from .models import Event, Ticket, Post, Notification


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'location', 'image']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'event', 'purchase_date', 'is_active', 'is_published']
        read_only_fields = ['purchase_date', 'is_published']  # Поле is_published остаётся только для чтения

    def create(self, validated_data):
        # Билет становится активным и публикуется
        validated_data['is_active'] = True
        validated_data['is_published'] = True
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'event', 'content', 'created_at', 'image']

    def create(self, validated_data):
        # Создаём пост без привязки к пользователю
        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'created_at']