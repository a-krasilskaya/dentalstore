from django.contrib import admin

from feedback.models import CallOrderForm, SendMessageForm

admin.site.register(CallOrderForm)
admin.site.register(SendMessageForm)
