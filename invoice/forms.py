from django import forms
from .models import Client, ClientIdentification, Premium, PremiumType, StatusType, Invoices
from django.core.exceptions import ValidationError




#   PInvoice
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoices
        fields = ['id', 'Client_ID', 'Premium_ID', 'unit', 'date', 'optional']

    name =forms.CharField()

    Client_ID =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['Client_ID']=forms.ModelChoiceField(queryset=Client.objects.all())

    Premium_ID =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )
    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.fields['Premium_ID']=forms.ModelChoiceField(queryset=Premium.objects.all())

    unit =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'units',
        })
    )
    date =forms.DateField(
        help_text="Due Date for Invoice",
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
class PremiumForm(forms.ModelForm):
    class Meta:
        model = Premium
        fields = ['Client_ID','LU_Premium_ID', 'LU_Status_ID', 'effective_date', 'expiration_date', 'dollar_amount']

    Client_ID =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )
    def __init__(self, *args, **kwargs):
        super(PremiumForm, self).__init__(*args, **kwargs)
        self.fields['Client_ID']=forms.ModelChoiceField(queryset=Client.objects.all())

    LU_Premium_ID =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )
    def __init__(self, *args, **kwargs):
        super(PremiumForm, self).__init__(*args, **kwargs)
        self.fields['LU_Premium_ID']=forms.ModelChoiceField(queryset=PremiumType.objects.all())

    LU_Status_ID =forms.CharField(

        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )
    def __init__(self, *args, **kwargs):
        super(PremiumForm, self).__init__(*args, **kwargs)
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
class PremiumTypeForm(forms.ModelForm):
    class Meta:
        model = PremiumType
        fields = ['name']

    name =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
        })
    )

