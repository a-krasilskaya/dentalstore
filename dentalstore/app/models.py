from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок', null=True,  blank=True)
    text = models.TextField(verbose_name='Текст', null=True, blank=True)
    image = models.ImageField(upload_to='static/app/images/bunner', verbose_name='Изображение')
    alt = models.CharField(max_length=255, verbose_name='Alt', null=True, blank=True)
    link = models.CharField(max_length=255, verbose_name='Ссылка', null=True,  blank=True)
    publish = models.BooleanField(verbose_name='Опубликовано', default=True)
    first_image = models.BooleanField(verbose_name='Установить как первое изображение слайда', default=True)


    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

    def __str__(self):
        return f'{self.title}'


class Sertificate(models.Model):
    name = models.CharField(max_length=255, verbose_name='Заголовок', null=True,  blank=True)
    image_name = models.ImageField(upload_to='static/uploads/images')

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

    def __str__(self):
        return f'{self.name}'