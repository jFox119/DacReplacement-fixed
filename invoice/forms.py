from django import forms
from .models import Client, ClientIdentification, ClientPremium, Premium, StatusType, Invoice
from django.core.exceptions import ValidationError

class DaisyUIDateInput(forms.DateInput):
    # Set the input type to 'date' to use the browser's native date picker
    input_type = 'date' 

    def __init__(self, attrs=None, format=None):
        # Define the default DaisyUI classes
        default_classes = "input input-bordered input-md w-full"
        
        # Combine default classes with any custom classes passed in attrs
        if attrs:
            if 'class' in attrs:
                attrs['class'] = f"{default_classes} {attrs['class']}"
            else:
                attrs['class'] = default_classes
        else:
            attrs = {'class': default_classes}
            
        # Ensure Django handles the format correctly for type="date"
        # The HTML5 date input type requires format='%Y-%m-%d' for proper validation
        super().__init__(attrs=attrs, format='%Y-%m-%d')


#   Invoice
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['invoice_id', 'is_paid', 'paid_amount','paid_date']
        #fields = ['invoice_id', 'client_premium', 'unit', 'date', 'optional', 'is_paid', 'paid_date']

    invoice_id =forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'input w-24',
            'disabled': 'disabled'
        })
    )

    is_paid = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'checkbox checkbox-sm checkbox-success'
            #'class': 'input input-bordered'
        })
    )
    paid_amount =forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'step': 0.01,
            'class': 'input input-bordered input-sm input-success',
            'placeholder': '0.00',
        })
    )
    paid_date = forms.DateField(
        label="Payment Date",
        widget=DaisyUIDateInput(attrs={'placeholder': 'DD-MM-YYYY',
                                    'class': 'input input-bordered input-sm input-success w-40'
        }),
        # Also include the input format in the field for validation purposes if needed
        input_formats=['%d-%m-%Y'],
    )
    '''
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
    '''

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

