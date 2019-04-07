from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from events.models import event, invitation, eventreq
from groups.models import *


# Create your views here.
def index(request):
    events = event.objects.all()
    query = request.GET.get('q')
    if query:
        events = event.objects.filter(name__icontains=query)
        print(events.query)
        if not events:
            events = event.objects.filter(venue__icontains=query)
    else:
        events = event.objects.all()

    return render(request, 'home/landing.html', {'events': events})


@login_required(login_url="/home/login")
def dashboard(request):
    # events = event.objects.all()
    events = event.objects.raw("select * from events_event")

    # invites = invitation.objects.filter(to=request.user)
    invites = invitation.objects.raw("select * from events_invitation where to_id = %s and status = %s",[request.user.id,0])

    # group = Group.objects.all()
    group = Group.objects.raw("select * from groups_Group")

    # group_invites = Group_invite.objects.filter(to=request.user)
    group_invites = Group_invite.objects.raw("select * from groups_Group_invite where to_id = %s and status = %s", [request.user.id,0])

    # grp = Group.objects.filter(creator=request.user)
    # grp = Group.objects.raw("select * from groups_Group where creator_id = %s",[request.user.id])
    #
    # group_requests_rcvd = Group_request.objects.none()
    #
    # for g in grp:
    #     if Group_request.objects.filter(group=g).exists():
    #         group_requests_rcvd |= Group_request.objects.filter(group=g, request_status=0)

    group_requests_rcvd = Group_request.objects.raw(
        "select * from groups_Group_request where group_id in (select id from groups_Group where creator_id = %s) and request_status=%s",[request.user.id,0])
    # print(group_requests_rcvd[0])
    # sent_group_requests = Group_request.objects.filter(request_from=request.user, request_status=0)

    sent_group_requests = Group_request.objects.raw("select * from groups_group_request where request_status = %s and request_from_id = %s",[0,request.user.id])

    send_requests_group = Group.objects.raw(
        'select * from groups_group where id not in(select group_id as id from groups_group_request where request_from_id = %s union select group_id as id from groups_group_members where user_id = %s)',[request.user.id,request.user.id])

    # send_requests_group = Group.objects.none()
    # for i in group:
    #     if (not Group.objects.filter(name=i.name, members=request.user).exists() and not Group_request.objects.filter(
    #             group=i, request_from=request.user).exists()):
    #         send_requests_group |= Group.objects.filter(name=i.name)

    # already_req = Group_request.objects.raw("select * from groups_group_request where group_")
    #


    # send_requests_group = Group.objects.raw(
    #     "select * from groups_Group as g1 where g1_id not in (select id from groups_group as g2 where g1.name=g2.name and g1.members_id = %s) and g1_id not in (select g3_id from groups_group_request where g1_id = g3_group_id and g3_request_from = %s)",[request.user.id,request.user.id])

    eventrequest = eventreq.objects.raw(
        "select * from events_eventreq where event_id in (select id from events_event where user_id = %s) and status = %s",
        [request.user.id, 'False'])

    return render(request, 'home/homepage.html',
                  {'events': events, 'invites': invites,'group_invites': group_invites,
                   'sent_group_requests': sent_group_requests,
                   'send_group_request': send_requests_group, 'group_requests_rcvd': group_requests_rcvd,
                   'eventreq': eventrequest})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home:dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'home/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'home/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home:index')
    else:
        logout(request)
        return redirect('home:index')
