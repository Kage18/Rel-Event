from django.shortcuts import render
from .forms import EventForm
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url="/accounts/login")
def eventView(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save(request)

    else:
        form = EventForm()
    return render(request, 'events/events.html', {'form': form})
