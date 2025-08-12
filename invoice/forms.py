from django import forms
from .models import Client
from django.core.exceptions import ValidationError



class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = (
            'first_name', 'last_name', 'address', 'city', 'state', 'zipcode'
        )

    first_name =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'first Name',
        })
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        # Check if the email already exists for this user
        if name.startswith('X'):
            raise ValidationError("No names beginning with X!")
        return name
    
    last_name =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'last Name'
        })
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        # Check if the email already exists for this user
        if name.startswith('X'):
            raise ValidationError("No names beginning with X!")
        return name

    address =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'address'
        })
    )
    city =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'city'
        })
    )
    state =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'state'
        })
    )
    zipcode =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'zipcode'
        })
    )
    