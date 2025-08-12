
from django.shortcuts import render
from django.http import HttpResponse
from .models import Client, ClientIdentification, Premium, PremiumType, StatusType

from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic.edit import FormMixin

from django.views.decorators.http import require_http_methods
from invoice.forms import ClientForm



#@login_required
def index(request):

    return render(request, 'invoice.html')

class ClientListView(generic.ListView, FormMixin):
    model = Client
    paginate_by = 2
    form_class = ClientForm
    template_name = 'client_list.html'

class ClientDetailView(generic.DetailView):
    model = Client


class ClientUpdateView(generic.UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'edit-client-modal.html'




@login_required
@require_http_methods(['POST'])
def edit_client(request):
    form = ClientForm(request.POST, initial={'user': request.user})
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
        # return partial containing a new row for our user
        # that we can add to the table
        context = {'contact': contact}
        response =  render(request, 'partials/contact-row.html', context)
        response['HX-Trigger'] = 'success'
        return response
    else:
        response =  render(request, 'partials/add-contact-modal.html', {'form': form})
        response['HX-Retarget'] = '#contact_modal'
        response['HX-Reswap'] = 'outerHTML'
        response['HX-Trigger-After-Settle'] = 'fail'

        return response
