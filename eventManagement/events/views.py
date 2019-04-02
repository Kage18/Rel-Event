from django.shortcuts import render,redirect
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from .models import invitation,event
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import connection


# Create your views here.

@login_required(login_url="/accounts/login")
def eventView(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(request)
            for k in form.cleaned_data['invite_users']:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO events_invitation (event_id,sender_id,to_id,msg,status) VALUES( %s , %s , %s, %s, %s)", [event.id, request.user.id, k, form.cleaned_data['message'], 'False'])
                cursor.close()
    else:
        form = EventForm()
    return render(request, 'events/events.html', {'form': form})


def accept_invite(request, pk):
    if pk:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE events_invitation SET status = %s WHERE id = %s", [1, pk])
            invite = invitation.objects.raw('select * from events_invitation where id = %s', [pk])[0]
            cursor.execute("INSERT INTO events_event_registered_users(event_id, user_id) VALUES( %s , %s )", [invite.event_id, invite.to_id])
            cursor.close()
    return redirect(reverse('accounts:home'))


