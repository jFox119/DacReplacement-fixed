from django import forms
from .models import Client, ClientIdentification, ClientPremium, Premium, StatusType, Invoice
from django.core.exceptions import ValidationError




#   Invoice
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_id', 'client_premium', 'unit', 'date', 'optional']


    unit =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'units',
        })
    )
    date =forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )
    optional =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Notes/Comments',
        })
    )


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'address']

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


#   Premiums
class ClientPremiumForm(forms.ModelForm):
    class Meta:
        model = ClientPremium
        fields = ['client','premium', 'LU_Status_ID', 'effective_date', 'expiration_date', 'dollar_amount']

    Client_ID =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )
    def __init__(self, *args, **kwargs):
        super(ClientPremiumForm, self).__init__(*args, **kwargs)
        self.fields['Client_ID']=forms.ModelChoiceField(queryset=Client.objects.all())

    LU_Premium_ID =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )
    def __init__(self, *args, **kwargs):
        super(ClientPremiumForm, self).__init__(*args, **kwargs)
        self.fields['LU_Premium_ID']=forms.ModelChoiceField(queryset=Premium.objects.all())

    LU_Status_ID =forms.CharField(

        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )
    def __init__(self, *args, **kwargs):
        super(ClientPremiumForm, self).__init__(*args, **kwargs)
        self.fields['LU_Status_ID']=forms.ModelChoiceField(queryset=StatusType.objects.all())

    effective_date =forms.DateField(
        help_text="Start date for premium",
        widget=forms.DateInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )

    expiration_date =forms.DateField(
        help_text="Start date for premium",
        widget=forms.DateInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )

    dollar_amount =forms.FloatField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )


#   Premium Type
class PremiumForm(forms.ModelForm):
    class Meta:
        model = Premium
        fields = ['name']

    name =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )

