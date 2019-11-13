from django.shortcuts import HttpResponseRedirect, render, reverse
from django.utils import timezone

from .models import Tickets


def index(request):
    html = 'index.html'

    ticket = Tickets.objects.all()

    return render(request, html, {'ticket': ticket})
    