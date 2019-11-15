from django.shortcuts import HttpResponseRedirect, render, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Tickets
from .forms import AddingNewTicketForm, LoginForm


def index(request):
    html = 'index.html'

    new = Tickets.objects.filter(
        ticket_status='New').order_by('-post_date')
    in_progress = Tickets.objects.filter(
        ticket_status='In Progress').order_by('-post_date')
    done = Tickets.objects.filter(
        ticket_status='Done').order_by('-post_date')
    invalid = Tickets.objects.filter(
        ticket_status='Invalid').order_by('-post_date')

    return render(request, html, {
        'new': new,
        'in_progress': in_progress,
        'done': done,
        'invalid': invalid
        })


# @login_required
def NewTicketFormView(request):
    html = 'genericform.html'

    if request.method == 'POST':
        form = AddingNewTicketForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Tickets.objects.create(
                title=data['title'],
                description=data['description'],
                ticket_status=data['ticket_status'],
                created_by=request.user,
                assigned_by=data['assigned_by']
            )
            return HttpResponseRedirect(reverse('homepage'))

    form = AddingNewTicketForm()

    return render(request, html, {'form': form})


def dev_person_view(request, id):
    html = 'devperson.html'

    created = Tickets.objects.filter(created_by=id)
    assigned = Tickets.objects.filter(assigned_by=id)
    completed = Tickets.objects.filter(completed_by=id)

    return render(request, html,
                  {'created': created,
                   'assigned': assigned,
                   'completed': completed})


def TicketDetailView(request, id):
    html = 'ticket.html'

    ticket = Tickets.objects.filter(id=id)

    return render(request, html, {'ticket': ticket})


def LoginView(request):
    html = 'genericform.html'

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                username=data['username'],
                password=data['password']
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get(
                        'next',
                        reverse('homepage')
                    )
                )

    form = LoginForm()

    return render(request, html, {'form': form})


def LogoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


def EditTicketView(request, id):
    html = 'genericform.html'

    instance = Tickets.objects.get(id=id)

    if request.method == 'POST':
        form = AddingNewTicketForm(
            request.POST,
            instance=instance
            )
        form.save()

        if instance.ticket_status == 'Done':
            instance.completed_by = instance.assigned_by
            instance.assigned_by = None
            form.save()
        elif instance.ticket_status == 'Invalid':
            instance.assigned_by = None
            instance.completed_by = None
            form.save()
        elif instance.ticket_status == 'In Progress' and instance.assigned_by is None:
            instance.assigned_by = instance.created_by
            instance.completed_by = None
            form.save()
        elif instance.assigned_by is not None:
            instance.ticket_status = 'In Progress'
            instance.completed_by = None
            form.save()


        return HttpResponseRedirect(reverse('homepage'))

    form = AddingNewTicketForm(instance=instance)

    return render(request, html, {'form': form})
