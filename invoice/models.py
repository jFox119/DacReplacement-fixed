from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse  # To generate URLS by reversing URL patterns
from simple_history.models import HistoricalRecords


# Create your models here.
class Client(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    #dacNumber = models.IntegerField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=5)
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}' 
    
    def get_absolute_url(self):
        """Returns the url to access a particular client record."""
        return reverse("invoice:client_detail", kwargs={"pk": self.pk})
    
class IdentificationType(models.Model):
    name = models.CharField(max_length=100)


    class Meta:
        db_table = "LU_Identification"
        verbose_name = 'Identification Type'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}' 
    
    #def get_absolute_url(self):
    #    """Returns the url to access a particular client record."""
    #    return reverse("invoice:client_detail", kwargs={"pk": self.pk})

class StatusType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "LU_Status"
        verbose_name = 'Status Type'
        verbose_name_plural = 'Status Types'
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}' 
    
    #def get_absolute_url(self):
    #    """Returns the url to access a particular client record."""
    #    return reverse("invoice:client_detail", kwargs={"pk": self.pk})

class DueDateType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "LU_DueDate"
        verbose_name = 'Due Date Type'
        verbose_name_plural = 'Due Date Types'
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}' 
    
    #def get_absolute_url(self):
    #    """Returns the url to access a particular client record."""
    #    return reverse("invoice:client_detail", kwargs={"pk": self.pk})

class ClientIdentification(models.Model):
    Client_ID = models.ForeignKey(Client, on_delete=models.PROTECT)
    LU_Identification_ID = models.ForeignKey(IdentificationType, on_delete=models.PROTECT, verbose_name="Identification Name")
    value = models.CharField(max_length=20)
    LU_Status_ID = models.ForeignKey(StatusType, on_delete=models.PROTECT, verbose_name="Status")
    effective_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        db_table = "Client_Identification"
        verbose_name = 'Client Identification'
    
    
    #def get_absolute_url(self):
    #    """Returns the url to access a particular client record."""
    #    return reverse("invoice:client_detail", kwargs={"pk": self.pk})

class ITEMCHANGES(models.Model):
    table_name = models.CharField(max_length=100)
    row_id = models.IntegerField()
    field_name = models.CharField(max_length=100)
    old_value = models.CharField(max_length=100)
    new_value = models.CharField(max_length=100)
    change_date = models.DateField(null=True, blank=True)
    USER_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                             related_name='employees')

    class Meta:
        db_table = "ITEM_CHANGES"
        verbose_name = 'ITEM CHANGES'
        verbose_name_plural = 'ITEM CHANGES'
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.transaction_id}, {self.table_name}, {self.change_date}' 
    
    #def get_absolute_url(self):
    #    """Returns the url to access a particular client record."""
    #    return reverse("invoice:client_detail", kwargs={"pk": self.pk})

class Premium(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}' 
    
    #def get_absolute_url(self):
    #    """Returns the url to access a particular premium record."""
    #    return reverse("invoice:premiumtype_detail", kwargs={"pk": self.pk})

class ClientPremium(models.Model):

    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    premium = models.ForeignKey(Premium, on_delete=models.PROTECT)

    LU_Status_ID = models.ForeignKey(StatusType, on_delete=models.PROTECT)
    effective_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    dollar_amount = models.FloatField(max_length=20)
    history = HistoricalRecords()


    def __str__(self):
        """String for representing the Model object."""
        return f'{self.client} : {self. premium}' 
    

    def get_absolute_url(self):
        """Returns the url to access a particular premium record."""
        return reverse("invoice:premium_detail", kwargs={"pk": self.pk})
        
class Invoice(models.Model):

    invoice_id = models.AutoField(primary_key=True)
    date = models.DateField() 
    client_premium = models.ForeignKey(ClientPremium, on_delete=models.CASCADE)
    unit = models.IntegerField()
    optional = models.CharField(max_length=200, null=True, blank=True)
    duedate = models.ForeignKey(DueDateType, on_delete=models.CASCADE)
    is_paid = models.BooleanField(null=True, blank=True, default=False)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)
    history = HistoricalRecords()


    class Meta:
        db_table = "Invoices"
        verbose_name = 'Invoices'
        verbose_name_plural = 'Invoices'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.invoice_id}' 
    
    def get_absolute_url(self):
        """Returns the url to access a particular invoice record."""
        return reverse("invoice:invoice_detail", kwargs={"pk": self.pk})
    
