from django.contrib import admin

from apps.coreApp.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Payment)
admin.site.register(Subscription)
admin.site.register(Message)
admin.site.register(Content)
admin.site.register(Tag)