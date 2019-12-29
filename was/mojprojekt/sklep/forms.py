from django.forms import ModelForm

from .models import Order, Complaint, Opinion


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['name', 'address', 'delivery']


class ComplaintForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['name', 'message']


class OpinionForm(ModelForm):
    class Meta:
        model = Opinion
        fields = ['comment', 'grade']
