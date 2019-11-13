from django import forms
from .models import Tickets


class AddingNewTicketForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = [
            'title',
            'description',
            'ticket_status'
        ]
        widgets = {
            'ticket': forms.RadioSelect
        }


form = AddingNewTicketForm()
