from django.contrib import admin
from invoice.models import  Client, IdentificationType, StatusType, ClientIdentification, ITEMCHANGES, PremiumType, Premium, Invoices

# Register your models here.
admin.site.register(ITEMCHANGES)
admin.site.register(Client)
admin.site.register(StatusType)
admin.site.register(IdentificationType)
#admin.site.register(ClientIdentification)
admin.site.register(PremiumType)

class ClientAdmin(admin.TabularInline):
    model = Client
    extra = 0
#admin.site.register(Client, ClientAdmin)

class StatusTypeAdmin(admin.TabularInline):
    model = StatusType
    extra = 0
#admin.site.register(StatusType, StatusTypeAdmin)

class IdentificationTypeAdmin(admin.TabularInline):
    model = IdentificationType
    extra = 0
#admin.site.register(IdentificationType, IdentificationTypeAdmin)

class ClientIdentificationAdmin(admin.ModelAdmin):
    list_display = ("Client_ID","LU_Identification_ID", "LU_Status_ID")

admin.site.register(ClientIdentification, ClientIdentificationAdmin)

class PremiumTypeAdmin(admin.TabularInline):
    model = PremiumType
    extra = 0
#admin.site.register(PremiumType,PremiumTypeAdmin)

class PremiumAdmin(admin.ModelAdmin):
    list_display = ("Client_ID","LU_Premium_ID", "LU_Status_ID")

    #fields = ["Client_ID","LU_Premium_ID", "LU_Status_ID"]
admin.site.register(Premium, PremiumAdmin)
admin.site.register(Invoices)
   
