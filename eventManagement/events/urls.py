from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('create/', views.eventView, name='createevent'),
    path('accept/<int:pk>', views.accept_invite, name='accept'),

]
