from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('clients/', views.ClientListView.as_view(), name='clients'),
    path('clients/<int:pk>', views.ClientDetailView.as_view(), name='client-detail'),
    path('clients_edit/', views.ClientUpdateView.as_view(), name='client-edit'),
    #path('edit_client/', views.edit_client, name='edit-client'),
]