from django import forms
from profile_dashboard.models import ticket_discussion

class TicketDiscussionForm(forms.ModelForm):
    class Meta:
        model = ticket_discussion
        fields = ['message', 'file_upload']
