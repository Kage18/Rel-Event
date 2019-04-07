from django.urls import path
from . import views
app_name = 'groups'

urlpatterns = [
    path('page/<int:pk>/', views.grp_page, name='grp-page'),
    path('create/', views.groupview, name='creategroup'),
    path('sendr/', views.sendr, name='sendr'),
    path('accept/<int:pk>', views.accept_invite, name='accept'),
    path('accept-req/', views.accept_req, name='accept_req'),
    path('decline-req/', views.decline_req, name='decline_req'),

]
