from django.urls import path

from . import views

app_name = "invoice"
urlpatterns = [
    path("", views.index, name="index"),
    path('invoice/', views.Invoices, name='invoice'),
    path('invoice/invoice_list', views.InvoiceListView.as_view(), name='invoice_list'),
    path("invoice/<int:pk>", views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoice/<int:pk>/edit/', views.InvoiceUpdateView.as_view(), name='invoice_edit'),

    path('clients/', views.clients, name='clients'),
    path('clients/client_list', views.ClientListView.as_view(), name='client_list'),
    path("clients/<int:pk>", views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_edit'),

    path('premiums/', views.premiums, name='premiums'),
    path('premiums/premium_list', views.PremiumListView.as_view(), name='premium_list'),
    path("premiums/<int:pk>", views.PremiumDetailView.as_view(), name='premium_detail'),
    path('premiums/<int:pk>/edit/', views.PremiumUpdateView.as_view(), name='premium_edit'),

    path('premiumtypes/', views.premiumtypes, name='premiumtypes'),
    path('premiumtypes/premiumtype_list', views.PremiumTypeListView.as_view(), name='premiumtype_list'),
    path("premiumtypes/<int:pk>", views.PremiumTypeDetailView.as_view(), name='premiumtype_detail'),
    path('premiumtypes/<int:pk>/edit/', views.PremiumTypeUpdateView.as_view(), name='premiumtype_edit'),

    path("pdf/<int:pk>", views.generate_pdf_report, name="pdfAuthors"),


    #path("clients/edit/<int:pk>", views.ClientEditView.as_view(), name="client_edit"),
    


    #path("clients/add/", views.ClientCreateView.as_view(), name="client-add"),
    #path("clients/<int:pk>/", views.ClientUpdateView.as_view(), name='client-update'),
    #path("clients/<int:pk>/delete/", views.ClientDeleteView.as_view(), name='client-delete'),
    #path('edit_client/', views.edit_client, name='edit-client'),
]