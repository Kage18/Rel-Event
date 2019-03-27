from django.shortcuts import render
from .forms import EventForm
from django.contrib.auth.decorators import login_required
from .models import invitation
from django.contrib.auth.models import User

# Create your views here.

@login_required(login_url="/accounts/login")
def eventView(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(request)
            for k in form.cleaned_data['invite_users']:
                user = User.objects.get(id=k)
                invite = invitation.objects.create(sender=request.user, to=user)
                invite.msg = form.cleaned_data['message']
                invite.event = event
                invite.save()
    else:
        form = EventForm()
    return render(request, 'events/events.html', {'form': form})
