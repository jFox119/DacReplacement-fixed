from django.contrib import admin
from invoice.models import  Client, IdentificationType, StatusType, ClientIdentification, ITEMCHANGES, PremiumType, Premium

# Register your models here.
admin.site.register(Client)
admin.site.register(IdentificationType)
admin.site.register(StatusType)
admin.site.register(ClientIdentification)
admin.site.register(ITEMCHANGES)
admin.site.register(PremiumType)
admin.site.register(Premium)

