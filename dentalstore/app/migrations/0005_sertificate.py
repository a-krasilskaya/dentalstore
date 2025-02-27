# Generated by Django 4.0 on 2024-05-05 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_banner_first_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sertificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Заголовок')),
                ('image_name', models.ImageField(upload_to='static/uploads/images')),
            ],
            options={
                'verbose_name': 'Сертификат',
                'verbose_name_plural': 'Сертификаты',
            },
        ),
    ]
