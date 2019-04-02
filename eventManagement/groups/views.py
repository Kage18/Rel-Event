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
            # group = form.save(request)
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO groups_group(name, description, creator_id) VALUES (%s,%s,%s)",
                               [form.cleaned_data['name'], form.cleaned_data['description'], request.user.id])
                gid = cursor.lastrowid
                cursor.close()
            for k in form.cleaned_data['members']:
                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO groups_group_members(group_id,user_id) VALUES (%s,%s)", [(str)(gid), k.id])
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
            cursor.execute("INSERT INTO groups_group_members (group_id, user_id) VALUES( %s , %s )", [group.group_id, group.to_id])
            cursor.close()
    return redirect(reverse('accounts:home'))

