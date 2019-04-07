from django.contrib import admin
from .models import event,invitation,comment,eventreq
# Register your models here.
admin.site.register(event)
admin.site.register(invitation)
admin.site.register(comment)
admin.site.register(eventreq)