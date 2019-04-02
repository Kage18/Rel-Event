from django.shortcuts import render, redirect
from .forms import GroupsForm
from django.contrib.auth.decorators import login_required
from .models import Group_invite
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import connection
# Create your views here.

@login_required(login_url="/accounts/login")
def groupview(request):
    if request.POST:
        form = GroupsForm(request.POST)
        if form.is_valid():
            group = form.save(request)
            with connection.cursor() as cursor:
            # event = form.save(request)
                cursor.execute("INSERT INTO events_event (date,description,time,city,state,private,venue,name,user_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", [form.cleaned_data['date'], form.cleaned_data['description'], (str)(time), form.cleaned_data['city'], form.cleaned_data['state'],form.cleaned_data['private'], form.cleaned_data['venue'], form.cleaned_data['name'], request.user.id])
                eid = cursor.lastrowid
                cursor.close()
            for k in form.cleaned_data['to']:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO groups_group_invite (group_id,to_id,status) VALUES( %s , %s , %s)", [group.id, k, 'False'])
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

@login_required(login_url="/accounts/login")
def accept_invite(request, pk):
    if pk:
        invite = Group_invite.objects.get(id=pk)
        invite.status = True
        # thisevent=event.objects.get(id=invite.event.id)
        invite.group.members.add(invite.to)
        invite.save()

    return redirect(reverse('accounts:home'))

