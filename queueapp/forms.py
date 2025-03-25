from django import forms
from .models import Business,Queue

from .models import QueueParticipant




class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'email', 'phone', 'address']
class QueueParticipantForm(forms.ModelForm):
    class Meta:
        model = QueueParticipant
        fields = ['name', 'email' ]

class QueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = ['name']
class JoinQueueForm(forms.ModelForm):
    class Meta:
        model = QueueParticipant
        fields = ['name', 'email']
