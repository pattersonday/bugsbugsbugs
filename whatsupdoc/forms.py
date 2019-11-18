from django import forms
from .models import Tickets


class adding_new_ticket_form(forms.ModelForm):
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


form = adding_new_ticket_form()


class login_form(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
