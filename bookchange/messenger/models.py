from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from catalog.models import Book

# Во-первых чаты могут быть двух видов. Первый - это личная беседа двух человек. Второй вид - это коллективый чат. Реализован только диалог, чат будет потом но кирпичик уже сделан
class Chat(models.Model):
    DIALOG = 'D'
    CHAT = 'C'
    CHAT_TYPE_CHOICES = ((DIALOG, 'Dialog'), (CHAT, 'Chat'))

    type = models.CharField('Тип', max_length=1, choices=CHAT_TYPE_CHOICES, default=DIALOG)
    book = models.OneToOneField(Book, on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(User)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def get_absolute_url(self):
        return reverse('messenger-message', args=[str(self.id)])

    def __str__(self):
        return str(self.id)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField("Message")
    pub_date = models.DateTimeField("Date", default=timezone.now)
    is_readed = models.BooleanField("Прочитано", default=False)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['pub_date']

    def __str__(self):
        return self.message