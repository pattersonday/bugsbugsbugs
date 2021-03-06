from django.shortcuts import HttpResponseRedirect, render, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

from .models import Tickets
from .forms import adding_new_ticket_form, login_form


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


@login_required
def new_ticket_form_view(request):
    html = 'genericform.html'

    if request.method == 'POST':
        form = adding_new_ticket_form(request.POST)

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

    form = adding_new_ticket_form()

    return render(request, html, {'form': form})


@login_required
def dev_person_view(request, id):
    html = 'devperson.html'

    created = Tickets.objects.filter(created_by=id)
    assigned = Tickets.objects.filter(assigned_by=id)
    completed = Tickets.objects.filter(completed_by=id)

    return render(request, html,
                  {'created': created,
                   'assigned': assigned,
                   'completed': completed})


@login_required
def ticket_detail_view(request, id):
    html = 'ticket.html'

    ticket = Tickets.objects.filter(id=id)

    return render(request, html, {'ticket': ticket})


def login_view(request):
    html = 'genericform.html'

    if request.method == 'POST':
        form = login_form(request.POST)

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

    form = login_form()

    return render(request, html, {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def edit_ticket_view(request, id):
    html = 'genericform.html'

    instance = Tickets.objects.get(id=id)

    if request.method == 'POST':
        form = adding_new_ticket_form(
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

    form = adding_new_ticket_form(instance=instance)

    return render(request, html, {'form': form})
