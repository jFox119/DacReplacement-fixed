from django.contrib import admin
from invoice.models import  Client, IdentificationType, StatusType, DueDateType,ClientIdentification, ITEMCHANGES, ClientPremium, Premium, Invoice

# Register your models here.
admin.site.register(ITEMCHANGES)
admin.site.register(Client)
admin.site.register(StatusType)
admin.site.register(DueDateType)
admin.site.register(IdentificationType)
#admin.site.register(ClientIdentification)


class ClientAdmin(admin.TabularInline):
    model = Client
    extra = 0
#admin.site.register(Client, ClientAdmin)

class StatusTypeAdmin(admin.TabularInline):
    model = StatusType
    extra = 0
#admin.site.register(StatusType, StatusTypeAdmin)

class DueDateTypeAdmin(admin.TabularInline):
    model = DueDateType
    extra = 0
#admin.site.register(DueDateType, DueDateTypeAdmin)

class IdentificationTypeAdmin(admin.TabularInline):
    model = IdentificationType
    extra = 0
#admin.site.register(IdentificationType, IdentificationTypeAdmin)

class ClientIdentificationAdmin(admin.ModelAdmin):
    list_display = ("Client_ID","LU_Identification_ID", "LU_Status_ID")

admin.site.register(ClientIdentification, ClientIdentificationAdmin)

class PremiumAdmin(admin.TabularInline):
    model = Client
    extra = 0
admin.site.register(Premium)
class ClientPremiumAdmin(admin.ModelAdmin):
    list_display = ("client","premium", "LU_Status_ID")

    #fields = ["Client_ID","LU_Premium_ID", "LU_Status_ID"]
admin.site.register(ClientPremium, ClientPremiumAdmin)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', "client_name","premium_name")
    readonly_fields = ('invoice_id',)
    fields = ('invoice_id', "date","client_premium", "unit", "optional", "duedate", "is_paid", "paid_amount", "paid_date")

    def client_name(self, obj):
        if obj.client_premium and obj.client_premium.client:
            return f"{obj.client_premium.client.first_name} {obj.client_premium.client.last_name}"
        else:
            return "N/A"  # Or some other suitable default value
    def premium_name(self, obj):
        if obj.client_premium and obj.client_premium.premium:
            return f"{obj.client_premium.premium.name}"
        else:
            return "N/A"  # Or some other suitable default value

admin.site.register(Invoice, InvoiceAdmin)
   
