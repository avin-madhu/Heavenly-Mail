from django import forms
from .models import ScheduledEmail

class EmailForm(forms.ModelForm):
    class Meta:
        model = ScheduledEmail
        fields = ['recipient_name', 'recipient_email', 'subject', 'message', 'send_on']
        widgets = {
            'send_on': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
