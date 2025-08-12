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
        """Returns the url to access a particular book record."""
        return reverse('client-detail', args=[str(self.id)])
    
class IdentificationType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "LU_Identification"
        verbose_name = 'LU Identification'


class StatusType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "LU_Status"
        verbose_name = 'LU Status'
        verbose_name_plural = 'LU Statuses'


class ClientIdentification(models.Model):
    Client_ID = models.ForeignKey(Client, on_delete=models.CASCADE)
    value = models.FloatField(max_length=20)
    LU_Identification_ID = models.ForeignKey(IdentificationType, on_delete=models.CASCADE)
    LU_Status_ID = models.ForeignKey(StatusType, on_delete=models.CASCADE)
    effective_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "Client_Identification"
        verbose_name = 'Client Identification'

class ITEMCHANGES(models.Model):
    transaction_id = models.IntegerField()
    table_name = models.CharField(max_length=100)
    row_id = models.IntegerField()
    field_name = models.CharField(max_length=100)
    old_value = models.CharField(max_length=100)
    new_value = models.CharField(max_length=100)
    change_date = models.DateField(null=True, blank=True)
    USER_ID = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='employees')

    class Meta:
        db_table = "ITEM_CHANGES"
        verbose_name = 'ITEM CHANGES'
        verbose_name_plural = 'ITEM CHANGES'

class PremiumType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "LU_Premium"
        verbose_name = 'LU Premium'

class Premium(models.Model):
    LU_Premium_ID = models.ForeignKey(PremiumType, on_delete=models.CASCADE)
    LU_Status_ID = models.ForeignKey(StatusType, on_delete=models.CASCADE)
    effective_date = models.DateField(null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)
    dollar_amount = models.FloatField(max_length=20)

    class Meta:
        db_table = "Premium"
        verbose_name = 'Premium'
        

