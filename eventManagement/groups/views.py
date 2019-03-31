from django.shortcuts import render, redirect
from .forms import GroupsForm
from django.contrib.auth.decorators import login_required
from .models import Group_invite
from django.contrib.auth.models import User
from django.urls import reverse
# Create your views here.


def groupview(request):
    if request.POST:
        form = GroupsForm(request.POST)
        if form.is_valid():
            group = form.save(request)
            for k in form.cleaned_data['to']:
                user = User.objects.get(id=k)
                invite = Group_invite.objects.create(to=user)
                invite.group = group
                invite.save()

    else:
        form = GroupsForm()

    return render(request, 'groups/groups.html', {'form': form})

