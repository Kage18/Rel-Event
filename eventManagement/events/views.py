from django.shortcuts import render, redirect
from .forms import EventForm,ReviewForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import connection
from collections import namedtuple


# Create your views here.

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


@login_required(login_url="/dashboard/login")
def eventView(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO events_event (start_date,start_time,end_date,end_time,description,city,state,private,venue,name,user_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    [form.cleaned_data['start_date'],(str)(form.cleaned_data['start_time']),form.cleaned_data['end_date'], (str)(form.cleaned_data['end_time']),form.cleaned_data['description'],
                     form.cleaned_data['city'], form.cleaned_data['state'], form.cleaned_data['private'],
                     form.cleaned_data['venue'], form.cleaned_data['name'], request.user.id])
                eid = cursor.lastrowid
                cursor.close()

                for k in form.cleaned_data['invite_users']:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO events_invitation (event_id,sender_id,to_id,msg,status) VALUES( %s , %s , %s, %s, %s)",
                            [(str)(eid), request.user.id, k, form.cleaned_data['message'], 0])
                        cursor.close()
    else:
        form = EventForm()
    return render(request, 'events/events.html', {'form': form})


def EventDetails(request, pk):
    e = event.objects.raw("select * from events_event where id = %s", [pk])[0]
    sentreq = eventreq.objects.raw("select * from events_eventreq where event_id = %s and by_id = %s",
                                   [pk, request.user.id])
    invite = invitation.objects.raw("select * from events_invitation where event_id = %s and to_id = %s",
                                    [pk, request.user.id])
    flag = 0
    sent = 1
    admin = event.objects.get(id=pk).user.id
    print(admin)
    if request.user.id == admin:
        flag = 1
        e = event.objects.get(id=pk)
        eventrequest = eventreq.objects.filter(event=e)
        print(eventrequest)
        guests = regUser.objects.filter(event=e)
        print(guests)
        return render(request, 'events/details.html',
                      {'e': e, 'sent': 2, 'invite': invite, 'flag': flag, 'eventreq': eventrequest,'guests':guests})

    if len(sentreq) == 0:
        sent = 0
        return render(request, 'events/details.html', {'e': e, 'sent': sent , 'invite': invite,'flag':flag})



    return render(request, 'events/details.html', {'e': e, 'sent': sent, 'sentreq': sentreq[0],'flag':flag})


def PastEventDetails(request, pk):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        rate = request.POST['rating']
        print("Rating:",rate)
        if form.is_valid():
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO events_review (event_id,by_id,text,date,rating) VALUES (%s,%s,%s,%s,%s)",
                    [pk,request.user.id,form.cleaned_data['text'],p.now(),rate])
                cursor.close()


    e = event_archive.objects.raw("select * from events_event_archive where id = %s", [pk])[0]
    c = review.objects.raw("select * from events_review where event_id = %s", [pk])
    commentbyuser = review.objects.raw("select * from events_review where event_id = %s and by_id = %s", [pk,request.user.id])
    print(commentbyuser)
    flag = 0
    if len(commentbyuser) == 0:
        form = ReviewForm()
        print(len(commentbyuser))
        flag = 1
        return render(request, 'events/pasteventdetail.html', {'e': e, 'c': c, 'form': form,'flag':flag})
    return render(request, 'events/pasteventdetail.html', {'e': e, 'c': c,'flag':flag})


def send(request):
    if request.POST:
        id = request.POST['id']
        print('------------------------------', id)
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO events_eventreq (status, by_id, event_id) VALUES (%s,%s,%s)",
                           [0, request.user.id, id])
            eid = cursor.lastrowid
            print(eid)
            cursor.close()
        return render(request, 'events/send.html')


def accept_invite(request, pk):
    if pk:
        with connection.cursor() as cursor:
            cursor.execute("UPDATE events_invitation SET status = %s WHERE id = %s", [1, pk])
            # invite = invitation.objects.raw('select * from events_invitation where id = %s', [pk])[0]
            # cursor.execute("INSERT INTO events_event_registered_users(event_id, user_id) VALUES( %s , %s )",
            #                [invite.event_id, invite.to_id])
            # cursor.close()
    return redirect(reverse('home:dashboard'))


def acceptreq(request):
    if request.POST:
        pk = request.POST["pk"]
        with connection.cursor() as cursor:
            cursor.execute("UPDATE events_eventreq SET status = %s WHERE id = %s", [1, pk])
            # req = eventreq.objects.raw('select * from events_eventreq where id = %s', [pk])[0]
            # cursor.execute("INSERT INTO events_event_registered_users(event_id, user_id) VALUES( %s , %s )",
            #                [req.event_id, req.by_id])
            cursor.close()
        return render(request, 'events/reqaccept.html')


def deleteguest(request):
    if request.POST:
        pk = request.POST["pk"]
        eventid = request.POST["eventid"]
        ev = event.objects.get(id=eventid)
        us = User.objects.get(id=pk)
        print(regUser.objects.get(event=ev,user=us))
        with connection.cursor() as cursor:
            cursor.execute("DELETE from events_reguser WHERE event_id = %s AND user_id = %s", [eventid, pk])
            # req = eventreq.objects.raw('select * from events_eventreq where id = %s', [pk])[0]
            # cursor.execute("INSERT INTO events_event_registered_users(event_id, user_id) VALUES( %s , %s )",
            #                [req.event_id, req.by_id])
            cursor.close()
        return render(request, 'events/deleteguest.html')


def comment(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # with connection.cursor() as cursor:
            #     cursor.execute("INSERT INTO events_comment (event,by,text,user_id) VALUES (%s,%s,%s,%s)",[form.cleaned_data['event'], request.user,form.cleaned_data['text'], request.user.id])
            #     cursor.close()
            new_form = form.save(commit=False)
            new_form.by = request.user
            new_form.save()


    else:
        form = ReviewForm()
    return render(request, 'events/comment.html', {'form': form})


def pastevents(request):
    # past_event = event_archive.objects.raw('SELECT * FROM events_event_archive')
    past_event = event_archive.objects.all()
    print(past_event)
    return render(request, 'events/pastevents.html',{'pevent':past_event})