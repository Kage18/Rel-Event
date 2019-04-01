from django.contrib import admin
from .models import event,invitation,comment
# Register your models here.
admin.site.register(event)
admin.site.register(invitation)
admin.site.register(comment)