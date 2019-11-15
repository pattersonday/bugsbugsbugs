from django import forms
from .models import Tickets


class AddingNewTicketForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = [
            'title',
            'description',
            'ticket_status',
            'assigned_by'
        ]
        widgets = {
            'ticket': forms.RadioSelect
        }


form = AddingNewTicketForm()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
