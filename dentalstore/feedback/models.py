from django.db import models

class CallOrderForm(models.Model):
    name = models.CharField(verbose_name='Имя пользователя', max_length=200)
    phone = models.CharField(verbose_name='Телефон')
    consent = models.BooleanField(verbose_name='Согласие с политикой конфиденциальности', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Форма заказать звонок"
        verbose_name_plural = "Формы заказать звонок"


class SendMessageForm(models.Model):
    name = models.CharField(verbose_name='Имя пользователя', max_length=200)
    phone = models.CharField(verbose_name='Телефон')
    email = models.EmailField(verbose_name='Email')
    text_message = models.TextField(verbose_name='Сообщение')
    consent = models.BooleanField(verbose_name='Согласие с политикой конфиденциальности', default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Форма отправить сообщение"
        verbose_name_plural = "Формы отправить сообщение"
