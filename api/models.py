from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    start_date = models.DateTimeField(
        verbose_name="Дата начала",
        null=True,
        blank=True
    )
    end_date = models.DateTimeField(
        verbose_name="Дата окончания",
        null=True,
        blank=True
    )
    location = models.CharField(max_length=255, verbose_name="Место проведения")
    image = models.ImageField(upload_to="event_images/", null=True, blank=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"

    def __str__(self):
        return self.title


class Ticket(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_tickets",
        verbose_name="Мероприятие"
    )
    purchase_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата покупки",
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name="Активен"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликован"
    )

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"

    def __str__(self):
        return f"Билет на {self.event}"


class Post(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event_posts",
        null=True,
        blank=True,
        verbose_name="Мероприятие"
    )
    content = models.TextField(verbose_name="Содержание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    image = models.ImageField(
        upload_to="post_images/",
        null=True,
        blank=True,
        verbose_name="Изображение"
    )

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    def __str__(self):
        return f"Пост о {self.event}"

    def save(self, *args, **kwargs):
        # Если пост связан с мероприятием и изображение не указано, берем изображение из Event
        if self.event and not self.image:
            self.image = self.event.image
        super().save(*args, **kwargs)


class Notification(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок", default="Default Title")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self):
        return f"Уведомление: {self.title}"