from django.urls import path

from . import views

app_name = "invoice"
urlpatterns = [
    path("", views.index, name="index"),
    path('logout/', views.logoutView, name='logout'),
    path('searchInvoice/', views.searchInvoiceTable, name='searchInvoice'),
    path('searchClients/', views.searchClientsTable, name='searchClients'),
    path('filter/<int:pk>', views.filterTable, name='filter'),

    path('invoices/', views.invoices, name='invoices'),
    path('invoices/invoice_list', views.InvoiceListView.as_view(), name='invoice_list'),
    path("invoices/<int:pk>", views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoices/<int:pk>/edit/', views.InvoiceUpdateView.as_view(), name='invoice_edit'),

    path('get_Invoice_Table_Data/', views.get_Invoice_Table_Data, name='get_Invoice_Table_Data'),
    path('get_Client_Table_Data/', views.get_Client_Table_Data, name='get_Client_Table_Data'),


    path('clients/', views.clients, name='clients'),
    path('clients/client_list', views.ClientListView.as_view(), name='client_list'),
    path("clients/<int:pk>", views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_edit'),

    path('clientpremiums/', views.clientpremiums, name='clientpremiums'),
    path('clientpremiums/clientpremium_list', views.ClientPremiumListView.as_view(), name='clientpremium_list'),
    path("clientpremiums/<int:pk>", views.ClientPremiumDetailView.as_view(), name='clientpremium_detail'),
    path('clientpremiums/<int:pk>/edit/', views.ClientPremiumUpdateView.as_view(), name='clientpremium_edit'),

    path('premiums/', views.premiums, name='premiums'),
    path('premiums/premium_list', views.PremiumListView.as_view(), name='premium_list'),
    path("premiums/<int:pk>", views.PremiumDetailView.as_view(), name='premium_detail'),
    path('premiums/<int:pk>/edit/', views.PremiumUpdateView.as_view(), name='premium_edit'),

    path("pdf/<int:pk>", views.pdfMultipleInvoices, name="pdfMultipleInvoices"),
    path("pdf/statement/<int:pk>", views.pdfSingleInvoice, name="pdfSingleInvoice"),

    path('load_Client_Invoices/<int:pk>', views.load_Client_Invoices, name='load_Client_Invoices'),
    path('load_Invoice_Payment/<int:pk>', views.load_Invoice_Payment, name='load_Invoice_Payment'),
    
    path('make_payment/<int:pk>/', views.make_payment, name='make_payment'),
    
    path('load_Payments/<int:pk>', views.load_Payments, name='load_Payments'),
    #path('manage_invoice/<int:pk>', views.manage_invoice, name='manage_invoice'),
    #path('load_Client_Invoices/', views.load_Client_Invoices, name='load_Client_Invoices'),
    


    #path("clients/edit/<int:pk>", views.ClientEditView.as_view(), name="client_edit"),
    


    #path("clients/add/", views.ClientCreateView.as_view(), name="client-add"),
    #path("clients/<int:pk>/", views.ClientUpdateView.as_view(), name='client-update'),
    #path("clients/<int:pk>/delete/", views.ClientDeleteView.as_view(), name='client-delete'),
    #path('edit_client/', views.edit_client, name='edit-client'),
]