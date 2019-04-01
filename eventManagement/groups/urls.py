from django.urls import path
from . import views
app_name = 'groups'

urlpatterns = [
    path('create/', views.groupview, name='creategroup'),
    path('accept/<int:pk>', views.accept_invite, name='accept'),

]
