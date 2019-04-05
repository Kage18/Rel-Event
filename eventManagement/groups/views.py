from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import GroupsForm
from django.contrib.auth.decorators import login_required
from .models import Group_invite
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import connection
from groups.models import *


# Create your views here.

@login_required(login_url="/accounts/login")
def groupview(request):
    if request.POST:
        form = GroupsForm(request.POST)
        if form.is_valid():
            # group = form.save(request)
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO groups_group(name, description, creator_id) VALUES (%s,%s,%s)",
                               [form.cleaned_data['name'], form.cleaned_data['description'], request.user.id])
                gid = cursor.lastrowid
                cursor.close()
            for k in form.cleaned_data['members']:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO groups_group_members(group_id,user_id) VALUES (%s,%s)",
                                   [(str)(gid), k.id])
                    cursor.close()
            for k in form.cleaned_data['to']:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO groups_group_invite (group_id,to_id,status) VALUES( %s , %s , %s)",
                                   [(str)(gid), k, 'False'])
                    cursor.close()
                # user = User.objects.get(id=k)
                # print('user: ', user.query)
                # invite = Group_invite.objects.create(to=user)
                # print('invite: ', invite.query)
                # invite.group = group
                # invite.save()

    else:
        form = GroupsForm()

    return render(request, 'groups/groups.html', {'form': form})


@login_required(login_url="/home/login")
def sendr(request):
    if request.method == 'POST':
        req = request.POST['req']
        receiver = Group.objects.get(id=req)

        print(receiver)
        if Group_request.objects.filter(group=receiver,request_from=request.user,request_status=2).exists():
            return render(request, "groups/request.html", {"message": 'You can not send request to this group'})


        elif Group.objects.filter(id=req, members=request.user).exists():
            print("Good one")
            return render(request, "groups/request.html", {"message": 'Already a member'})


        else:
            # print("Bad one")
            Group_request.objects.create(group=receiver, request_from=request.user, request_status=0)
            grp = Group.objects.get(id=req)
            return render(request, "groups/request_succ.html", {'grp': grp})


@login_required(login_url="/accounts/login")
def accept_invite(request, pk):
    if pk:
        # invite = Group_invite.objects.get(id=pk)
        # invite.status = True
        # # thisevent=event.objects.get(id=invite.event.id)
        # invite.group.members.add(invite.to)
        # invite.save()
        with connection.cursor() as cursor:
            cursor.execute("UPDATE groups_group_invite SET status = %s WHERE id = %s", [1, pk])
            group = Group_invite.objects.raw('select * from groups_group_invite where id = %s', [pk])[0]
            cursor.execute("INSERT INTO groups_group_members (group_id, user_id) VALUES( %s , %s )",
                           [group.group_id, group.to_id])
            cursor.close()
    return redirect(reverse('home:dashboard'))


@login_required(login_url="/home/login")
def accept_req(request):
    if request.method == 'POST':
        req = request.POST['req']
        sender = Group_request.objects.get(id=req)
        sender.request_status = 1
        sender.save()
        print(sender)
        print(Group.objects.filter(id=sender.group.id, members=sender.request_from))
        if Group.objects.filter(id=sender.group.id, members=sender.request_from).exists():
            print("Good one")
            return render(request, "groups/request.html", {"message": 'Already a member'})
        else:
            # print("Bad one")
            # Group_request.objects.create(group=receiver, request_from=request.user,request_status=False)
            print(sender.group.id)
            grp = Group.objects.get(id=sender.group.id)
            print(grp)
            print(sender.request_from)
            sender.group.members.add(sender.request_from)
            return render(request, "groups/request_acc.html", {'user': sender.request_from,'grp':grp,'message':'accepted'})


@login_required(login_url="/home/login")
def decline_req(request):
    if request.method == 'POST':
        req = request.POST['req']
        sender = Group_request.objects.get(id=req)
        sender.request_status = 2
        sender.save()
        print(sender)
        print(Group.objects.filter(id=sender.group.id, members=sender.request_from))
        try:
            return render(request, "groups/request_acc.html", {'user': sender.request_from,'grp':sender.group,'message':'declined'})
        except:
            return render(request, "groups/request_acc.html", {'message':'Error occured'})

