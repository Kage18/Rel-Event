from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    # path('',views.listEvent,name='list-event'),
    path('create/', views.eventView, name='createevent'),
    path('accept/<int:pk>', views.accept_invite, name='accept'),
    path('comment/', views.comment, name='comment'),
    path('detail/<int:pk>', views.EventDetails,name='details'),
    path('pastdetail/<int:pk>', views.PastEventDetails,name='pasteventdetails'),
    path('send/', views.send, name='send'),
    path('acceptreq/', views.acceptreq, name='acceptreq'),
    path('deleteguest/', views.deleteguest, name='deleteguest'),

    path('pastevents/', views.pastevents, name='pastevents'),

]
