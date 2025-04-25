from rest_framework import viewsets, permissions, generics
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .models import  Event, Ticket, Post, Notification
from .serializers import  EventSerializer, TicketSerializer, PostSerializer, NotificationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# Закомменчены регистрация и вход - раскомментируйте когда будете реализовывать
# class RegisterView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [permissions.AllowAny]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'user': UserSerializer(user).data,
#             'token': token.key
#         }, status=201)

# class LoginView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                          context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'user': UserSerializer(user).data,
#             'token': token.key
#         })

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AllowAny]  # Разрешаем доступ всем

    def perform_create(self, serializer):
        # Убираем привязку к пользователю
        serializer.save()

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [AllowAny]  # Разрешаем доступ всем

    def get_queryset(self):
        # Возвращаем все билеты, так как нет авторизации
        return Ticket.objects.all()

    @action(detail=True, methods=['post'], url_path='purchase')
    def purchase_ticket(self, request, pk=None):
        """
        Метод для приобретения билета.
        """
        try:
            ticket = Ticket.objects.get(pk=pk, is_published=True, user__isnull=True)
        except Ticket.DoesNotExist:
            return Response({"detail": "Билет недоступен для покупки."}, status=status.HTTP_404_NOT_FOUND)

        # Привязываем билет к "анонимному" пользователю (оставляем user пустым)
        ticket.user = None
        ticket.is_active = True
        ticket.is_published = False
        ticket.purchase_date = timezone.now()
        ticket.save()

        return Response({"detail": "Билет успешно приобретён."}, status=status.HTTP_200_OK)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().select_related('event')
    serializer_class = PostSerializer
    permission_classes = [AllowAny]  # Разрешаем доступ всем

    def perform_create(self, serializer):
        # Убираем привязку к пользователю
        serializer.save()

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [AllowAny]  # Разрешаем доступ всем

    # Убираем select_related('user'), так как поля user больше нет
    queryset = Notification.objects.all()

    def get_queryset(self):
        # Возвращаем все уведомления, так как нет привязки к пользователю
        return self.queryset

    def perform_create(self, serializer):
        # Убираем привязку к пользователю
        serializer.save()