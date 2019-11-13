from django.shortcuts import HttpResponseRedirect, render, reverse
from django.utils import timezone

from .models import Tickets
from .forms import AddingNewTicketForm


def index(request):
    html = 'index.html'

    ticket = Tickets.objects.all()

    return render(request, html, {'ticket': ticket})


def NewTicketFormView(request):
    html = 'newticket.html'

    if request.method == 'POST':
        form = AddingNewTicketForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Tickets.objects.create(
                title=data['title'],
                description=data['description'],
                ticket_status=data['ticket_status']
            )
            return HttpResponseRedirect(reverse('homepage'))

    form = AddingNewTicketForm()

    return render(request, html, {'form': form})
