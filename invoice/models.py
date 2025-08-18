from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse  # To generate URLS by reversing URL patterns


# Create your models here.


class Client(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=5)

    class Meta:
        db_table = "Client"
        verbose_name = 'Client'
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


class ClientIdentification(models.Model):
    Client_ID = models.ForeignKey(Client, on_delete=models.PROTECT)
    LU_Identification_ID = models.ForeignKey(IdentificationType, on_delete=models.PROTECT, verbose_name="Identification Name")
    value = models.CharField(max_length=20)
    LU_Status_ID = models.ForeignKey(StatusType, on_delete=models.PROTECT, verbose_name="Status")
    effective_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "Client_Identification"
        verbose_name = 'Client Identification'
    
    
    #def get_absolute_url(self):
    #    """Returns the url to access a particular client record."""
    #    return reverse("invoice:client_detail", kwargs={"pk": self.pk})

class ITEMCHANGES(models.Model):
    transaction_id = models.IntegerField()
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

class PremiumType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "LU_Premium"
        verbose_name = 'Premium Type'
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}' 
    
    def get_absolute_url(self):
        """Returns the url to access a particular client record."""
        return reverse("invoice:premiumtype_detail", kwargs={"pk": self.pk})

class Premium(models.Model):
    Client_ID = models.ForeignKey(Client, on_delete=models.PROTECT, blank=True, default="")
    LU_Premium_ID = models.ForeignKey(PremiumType, on_delete=models.PROTECT)
    LU_Status_ID = models.ForeignKey(StatusType, on_delete=models.PROTECT)
    effective_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    dollar_amount = models.FloatField(max_length=20)

    class Meta:
        db_table = "Client_Premium"
        verbose_name = 'Client Premium'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.Client_ID} : {self. LU_Premium_ID}' 
    

    def get_absolute_url(self):
        """Returns the url to access a particular premium record."""
        return reverse("invoice:premium_detail", kwargs={"pk": self.pk})
        


class Invoices(models.Model):
    Premium_ID = models.ForeignKey(Premium, on_delete=models.PROTECT)
    unit = models.IntegerField()
    date = models.DateField(null=True, blank=True)
    optional = models.CharField(max_length=200)


    class Meta:
        db_table = "Invoices"
        verbose_name = 'Invoices'
    

    
    def get_absolute_url(self):
        """Returns the url to access a particular invoice record."""
        return reverse("invoice:invoice_detail", kwargs={"pk": self.pk})
    
