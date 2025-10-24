from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Client, ClientIdentification, ClientPremium, Premium, StatusType, Invoice, Payments

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views import generic
from django.views.generic.edit import FormMixin

from django.views.decorators.http import require_http_methods
from invoice.forms import ClientForm, ClientPremiumForm, PremiumForm, InvoiceForm, PaymentsForm
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy, reverse

from django_htmx.http import HttpResponseClientRefresh

from datetime import date, datetime
from django.db.models import Q

# REPORT LAB
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from django.http import HttpResponse, FileResponse
from io import BytesIO


#@login_required
def index(request):
    return render(request, 'index.html')

class adminCheckView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponse("Welcome, Superuser!")
        else:
            return HttpResponse("You are not a superuser.")
        
def logoutView(request):
    logout(request)
    return redirect(reverse('logged_out'))

def searchInvoiceTable(request):
    import time
    time.sleep(2)
    search_query = request.GET.get('search', '')

    # Use select_related() to follow the foreign key relationships.
    # The double underscore syntax (`__`) is used to traverse these relationships.
    invoices = Invoice.objects.select_related(
        'client_premium__client', 
        'client_premium__premium'
    ).filter(
        Q(client_premium__client__first_name__icontains=search_query) | 
        Q(client_premium__client__last_name__icontains=search_query) |
        Q(client_premium__premium__name__icontains=search_query)
    ).order_by('date')

    #for item in invoices:
    #    client_first = item.client_premium.client.first_name
    #    prem = item.client_premium.premium.name
    #    print("c:", client_first, "--  p: ", prem)
    return render(request, 'invoice/invoice_list.html', {'invoices': invoices})


def searchClientsTable(request):
    import time
    time.sleep(2)
    search_query = request.GET.get('search', '')

    # Use select_related() to follow the foreign key relationships.
    # The double underscore syntax (`__`) is used to traverse these relationships.
    clients = Client.objects.filter(
        Q(first_name__icontains=search_query) | 
        Q(last_name__icontains=search_query) 
    ).order_by('last_name')

    #for item in invoices:
    #    client_first = item.client_premium.client.first_name
    #    prem = item.client_premium.premium.name
    #    print("c:", client_first, "--  p: ", prem)
    return render(request, 'invoice/client_list.html', {'clients': clients})


def filterTable(request, pk):
    import time
    time.sleep(1)
    #print(request)
    if request.method == 'POST':
        if 'filter' in request.POST:
            is_active = 'filter' in request.POST
            #print(is_active)
            if is_active:
                filter_query = get_object_or_404(Premium.objects.select_related(), pk=pk)
                #filter_query = request.GET.get('filter', '')

                # Use select_related() to follow the foreign key relationships.
                # The double underscore syntax (`__`) is used to traverse these relationships.
                invoices = Invoice.objects.select_related(
                    'client_premium__client', 
                    'client_premium__premium'
                ).filter(
                    Q(client_premium__client__first_name__icontains=filter_query) | 
                    Q(client_premium__client__last_name__icontains=filter_query) |
                    Q(client_premium__premium__name__icontains=filter_query)
                ).order_by('date')
                #for item in invoices:
                #    client_first = item.client_premium.client.first_name
                #    prem = item.client_premium.premium.name
                #    print("c:", client_first, "--  p: ", prem)
                return render(request, 'invoice/invoice_list.html', {'invoices': invoices})
        else:
            invoices = Invoice.objects.select_related('client_premium__client', 'client_premium__premium').all()
            form = InvoiceForm()
            premiums = Premium.objects.all()
            context = {
                'invoices': invoices,
                'form': form,
                'premiums': premiums,
            }
            return render(request, 'invoice/invoice_list.html', context)



def invoices(request):
    #invoices = Invoice.objects.select_related('client_premium__client', 'client_premium__premium').all()
    clients = Client.objects.all()
    #form = InvoiceForm()
    premiums = Premium.objects.all()
    context = {
        #'invoices': invoices,
        #'form': form,
        'premiums': premiums,
        'clients': clients
    }
    return render(request, 'invoices.html', context)


class InvoiceListView(generic.ListView):
    model = Invoice
    paginate_by = 2

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


class InvoiceDetailView(generic.DetailView):
    model = Invoice
    template_name = 'invoice/partials/invoice_form_partial.html' # Render only the form

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            #context['form'] = InvoiceForm(instance=self.object)
            return context


class InvoiceUpdateView(generic.UpdateView):
    model = Invoice
    form_class = InvoiceForm
    template_name = 'invoice/partials/invoice_form_partial.html'
    success_url = reverse_lazy('invoice:invoices')  # Or use get_success_url()

    def get_object(self, queryset=None):
            # This method is automatically called by UpdateView to retrieve the object
            # self.kwargs['pk'] will contain the primary key from the URL
            return super().get_object(queryset)

    # If you're using a FormView and need to pass the pk to the form's __init__
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['pk'] = self.kwargs['pk']  # Pass pk to the form
        return kwargs

    def form_valid(self, form):
        print("valid")
        # Process the form data (e.g., save to database)
        form.save()

        # Check if it's an HTMX request
        if self.request.headers.get('HX-Request'):
            return HttpResponseClientRefresh()
        else:
            return super().form_valid(form)

    def form_invalid(self, form):
        print("invalid")
        print(form.errors)
        #return super().form_invalid(form)
        return self.render_to_response(self.get_context_data(form=form))

def get_Invoice_Table_Data(request):
    selected_item_id = request.GET.get('client_id') # Get the selected value from the dropdown
    if selected_item_id and selected_item_id != 0:
        # Filter your model based on the selected item_id
        clients = Client.objects.filter(pk=selected_item_id).first()
        invoices = Invoice.objects.select_related('client_premium__client', 'client_premium__premium').filter(client_premium__client__id = selected_item_id).order_by('date')
        #form = InvoiceForm()
        premiums = Premium.objects.all()
        context = {
            'invoices': invoices,
            #'form': form,
            'premiums': premiums,
            'clients': clients
        }
    else:
        context = {} # Return an empty list if no item is selected

    return render(request, 'invoice/invoice_list.html', context)

def get_Client_Table_Data(request):
    selected_item_id = request.GET.get('client_id') # Get the selected value from the dropdown
    if selected_item_id and selected_item_id != 0:
        # Filter your model based on the selected item_id
        clients = Client.objects.filter(pk=selected_item_id)
        context = {
            'clients': clients
        }
    else:
        context = {} # Return an empty list if no item is selected

    return render(request, 'invoice/client_list.html', context)

def make_payment(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    print("called")
    print(invoice)
    if request.method == 'POST':
        form = PaymentsForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.invoice_id = invoice
            payment.save()
            
            # After successful payment, render a new row for the table or confirmation message.
            # You can send back an empty response to close the modal.
            return HttpResponse(status=204) # 204 No Content for a successful HTMX response
        else:
            print("invalid")
            print(form.errors)
            print(form.data)
            # If form is invalid, re-render the modal content with errors
            return render(request, 'invoice/partials/payment_modal_content.html', {'form': form, 'invoice': invoice})
    else:
        # For a GET request, render the initial form
        form = PaymentsForm(initial={'invoice': invoice})
    return render(request, 'invoice/partials/payment_modal_content.html', {'form': form, 'invoice': invoice})


class adminCheckView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponse("Welcome, Superuser!")
        else:
            return HttpResponse("You are not a superuser.")

def clients(request):
    ddlclients = Client.objects.all()
    form = ClientForm()
    years = []
    for i in range(2010, (datetime.now().year + 5)):
        years.append((i,i))
    context = {
        'ddlclients': ddlclients,
        'form': form,
        'years': years
    }
    return render(request, 'clients.html', context)


class ClientListView(generic.ListView):
    model = Client
    paginate_by = 2


class ClientDetailView(generic.DetailView):
    model = Client
    template_name = 'invoice/partials/item_form_partial.html' # Render only the form

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['form'] = ClientForm(instance=self.object)
            return context


class ClientUpdateView(generic.UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'invoice/partials/item_form_partial.html'
    success_url = reverse_lazy('invoice:clients')  # Or use get_success_url()

    def form_valid(self, form):
        # Process the form data (e.g., save to database)
        form.save()

        # Check if it's an HTMX request
        if self.request.headers.get('HX-Request'):
            return HttpResponseClientRefresh()
        else:
            return super().form_valid(form)

#   Premiums
def clientpremiums(request):
    premiums = ClientPremium.objects.all()
    form = ClientPremiumForm()
    context = {
        'premiums': premiums,
        'form': form,
    }
    return render(request, 'clientpremiums.html', context)


class ClientPremiumListView(generic.ListView):
    model = ClientPremium
    paginate_by = 2


class ClientPremiumDetailView(generic.DetailView):
    model = ClientPremium
    template_name = 'invoice/partials/clientpremium_form_partial.html' # Render only the form

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['form'] = PremiumForm(instance=self.object)
            return context


class ClientPremiumUpdateView(generic.UpdateView):
    model = ClientPremium
    form_class = ClientPremiumForm
    template_name = 'invoice/partials/clientpremium_form_partial.html'
    success_url = reverse_lazy('invoice:clientpremiums')  # Or use get_success_url()

    def form_valid(self, form):
        # Process the form data (e.g., save to database)
        form.save()

        # Check if it's an HTMX request
        if self.request.headers.get('HX-Request'):
            return HttpResponseClientRefresh()
        else:
            return super().form_valid(form)

#   Premium Types
def premiums(request):
    premiums = Premium.objects.all()
    form = PremiumForm()
    context = {
        'premiums': premiums,
        'form': form,
    }
    return render(request, 'premiums.html', context)


class PremiumListView(generic.ListView):
    model = Premium
    paginate_by = 2


class PremiumDetailView(generic.DetailView):
    model = Premium
    template_name = 'invoice/partials/premium_form_partial.html' # Render only the form

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['form'] = PremiumForm(instance=self.object)
            return context


class PremiumUpdateView(generic.UpdateView):
    model = Premium
    form_class = PremiumForm
    template_name = 'invoice/partials/premium_form_partial.html'
    success_url = reverse_lazy('invoice:premiums')  # Or use get_success_url()

    def form_valid(self, form):
        # Process the form data (e.g., save to database)
        form.save()

        # Check if it's an HTMX request
        if self.request.headers.get('HX-Request'):
            return HttpResponseClientRefresh()
        else:
            return super().form_valid(form)

#def load_Client_Invoices(request):
def load_Client_Invoices(request, pk):
    client = Client.objects.get(pk=pk)
    #client = Client.objects.get(pk=1)
    queryset = Invoice.objects.select_related('client_premium__client', 'client_premium__premium').filter(client_premium__client=client)
    
    context = {'queryset' : queryset, 'client': client}
    for item in queryset:
        print(item.client_premium)
    return render(request, 'invoice/partials/table_invoice_modal.html', context)

def load_Invoice_Payment(request, pk):
    invoice =  get_object_or_404(Invoice.objects.select_related('client_premium__client', 'duedate'), pk=pk)
    payment = get_object_or_404(Payments.objects.select_related('invoice__client_premium__client'), pk=pk)
    context = {'invoice': invoice,
               'payment': payment}

    return render(request, 'invoice/partials/invoice_payment_modal.html', context)
def load_Payments(request, pk):
    invoice = get_object_or_404(Invoice.objects.select_related('client_premium__client', 'duedate'), pk=pk)
    payments = Payments.objects.filter(invoice_id=pk)

    context = {'invoice': invoice,
               'payments': payments}

    return render(request, 'invoice/partials/invoice_payment_modal.html', context)


from django.db import transaction
def manage_invoice(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    # Filter the formset to only show payments for the current invoice instance
    queryset = Payments.objects.filter(invoice_id=pk)
    print("called")
    print(request.method)
  
    if request.method == 'POST':
        print("POST")
        formset = PaymentsForm(request.POST, queryset=queryset)
        if formset.is_valid():
            with transaction.atomic():
                # Save each form in the formset
                for form in formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                        payment = form.save(commit=False)
                        payment.invoice = invoice  # Link the payment to the specific invoice
                        payment.save()
                
                # Optional: Delete marked payments
                formset.save() 
                
                # You might want to recalculate invoice status/balance here
                
            return redirect('invoice/partials/manage_invoice.html', invoice_id=invoice.invoice_id)
    else:
        formset = PaymentsForm(queryset)

        
    return render(request, 'invoice/partials/manage_invoice.html', {'invoice': invoice, 'formset': formset})



from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame, BaseDocTemplate, PageTemplate, NextPageTemplate, PageBreak, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib import colors

from django.shortcuts import get_object_or_404
from weasyprint import HTML, CSS
from django.template.loader import render_to_string

def pdfMultipleInvoices(request,pk):
    invoiceData = get_object_or_404(Invoice.objects.select_related('client_premium__client', 'duedate'), pk=pk)
    client = invoiceData.client_premium.client
    #queryset = Invoice.objects.select_related('client_premium__client', 'client_premium__premium').filter(pk=pk)
    queryset = Invoice.objects.select_related('client_premium__client', 'client_premium__premium', 'duedate').filter(client_premium__client=client).order_by('invoice_id')
    
    itemtotal = 0
    total = 0
    for obj in queryset:
        itemtotal = (obj.unit * obj.client_premium.dollar_amount)
        total += itemtotal
    invMinID = queryset.first()
    invMaxID = queryset.last()


    html_string = render_to_string('weasyprint/multi-invoice.html', 
                                   {
                                       'invoice': invoiceData, 
                                        'client': client, 
                                        'queryset': queryset, 
                                        'total': total,
                                        'invMinID': invMinID,
                                        'invMaxID': invMaxID,
                                    }
    )
    #html_string = render_to_string('weasyprint/single_profile_pdf.html', {'client': client})

    response = HttpResponse(content_type="application/pdf")
    response["Content-Dispostition"] = f'inline; filename="{client.first_name}"'
    #response["Content-Dispostition"] = 'inline; filename="Bob.pdf"'

    HTML(string=html_string).write_pdf(response, stylesheets=['invoice/templates/weasyprint/invoice.css'])
    return response
'''
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # database data
    #   Using select_related to efficiently retrieve related objects
    #invoiceData = Invoice.objects.filter(pk = pk).first()
    #clientprem = ClientPremium.objects.filter(id = invoiceData.client_premium_id ).first()
    #client = Client.objects.filter(id = clientprem.client.id).first()
    #queryset = Invoice.objects.select_related('client_premium__client', 'client_premium__premium').filter(client_premium__client__id = clientprem.client.id)

    invoiceData = get_object_or_404(Invoice.objects.select_related('client_premium__client'), pk=pk)
    client = invoiceData.client_premium.client
    queryset = Invoice.objects.select_related('client_premium__client', 'client_premium__premium').filter(pk=pk)
    #queryset = Invoice.objects.select_related('client_premium__client', 'client_premium__premium').filter(client_premium__client=client)

    #  Iterate through the results to access the desired fields
    #for invoice in invoiceDate:
    #   print(f"Invoice ID: {invoice.invoice_id}, Premium Name: {invoice.client_premium.premium.name}, Client Name: {invoice.client_premium.client.first_name}, Date: {invoice.date}")
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5 * inch, leftMargin= .5 * inch)
    style = getSampleStyleSheet()
    headerStyle = ParagraphStyle('header',
                            fontName="Courier",
                            fontSize=12,
                            alignment=0,
                            spaceAfter=0
    )
    rightHeaderStyle = ParagraphStyle('rightHeader',
                            fontName="Courier",
                            fontSize=12,
                            spaceAfter=0,
                            alignment=TA_RIGHT
    )
    centerStyle = ParagraphStyle('rightHeader',
                            fontName="Courier",
                            fontSize=12,
                            spaceAfter=0,
                            alignment=1
    )

    story = []

    headerData = [
        [Paragraph("Appalachian Agency for Senior Citizens", headerStyle)],
        [Paragraph("P.O. Box 765", headerStyle), Paragraph("INVOICE", rightHeaderStyle)],
        [Paragraph("Cedar Bluff, VA 24609", headerStyle)]

    ]
    subtotal = invoiceData.unit * invoiceData.client_premium.dollar_amount
    queryData = [['Description', 'Quantity', 'Amount', 'Total Due']]
    for obj in queryset:
        queryData.append([obj.client_premium.premium.name, obj.unit, obj.client_premium.dollar_amount, subtotal])

    
    footerData = [
        [Paragraph("Notes/Comments", headerStyle), Paragraph("", centerStyle), Paragraph("Subtotal: " + " $" + f"{subtotal:,.2f}", rightHeaderStyle)],
        [Paragraph("", headerStyle),Paragraph("Thank you", centerStyle)],
        [Paragraph("", headerStyle),Paragraph("PLEASE MAKE CHECKS PAYABLE TO", centerStyle)],
        [Paragraph("", headerStyle),Paragraph("APPALACHIAN AGENCY FOR SENIOR CITIZENS", centerStyle)],
        [Paragraph("", headerStyle),Paragraph("", centerStyle),Paragraph("Total: " + " $" + f"{subtotal:,.2f}", rightHeaderStyle)]

    ]

    colWidths=[5 * inch, 2.0 * inch]
    headerTable = Table(headerData, colWidths=colWidths, rowHeights=5*mm)

    colWidths=[3 * inch, 2.0 * inch, 1 * inch, 1 * inch]
    table_style = TableStyle([
        ('FONTNAME', (0,0), (-1,0), 'Courier-Bold'), # Apply bold font to the first row
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black), # Line below the first
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black), # Line below the first
    ])
    queryTable = Table(queryData, colWidths=colWidths, rowHeights=6*mm)
    queryTable.setStyle(tblstyle=table_style)

    colWidths=[2 * inch, 3.25 * inch, 1.75 * inch]
    footerTable = Table(footerData, colWidths=colWidths)

    #   header
    story.append(headerTable)
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Phone : (276) 964-4915 Fax : (276) 963-0130", headerStyle))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(("Invoice Date: " +  str(invoiceData.date.strftime("%m-%d-%Y")) + "  Inv No: " + str(invoiceData.invoice_id)), rightHeaderStyle))
    #story.append(Paragraph(("Invoice Date: " +  str(date.today()) + "  Inv No: " + str(invoiceData.invoice_id)), rightHeaderStyle))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(("Due Date: " + str(invoiceData.duedate)), rightHeaderStyle))
    #story.append(Paragraph("Due Date: Monthly", rightHeaderStyle))
    story.append(Spacer(1, 0.3 * inch))

    # body
    story.append(Paragraph((client.first_name + " " + client.last_name), headerStyle))
    story.append(Paragraph(client.address, headerStyle))
    story.append(Paragraph((client.city + ", " + client.state + " " + client.zip), headerStyle))
    story.append(Spacer(1, .5 * inch))

    #  table
    story.append(Paragraph("DUE ON RECIEPT", centerStyle))
    story.append(Spacer(1, 0.1 * inch))
    story.append(queryTable)
    story.append(Spacer(1, 4.1 * inch))
    
    # footer
    story.append(footerTable)
    
    #story.append(Paragraph(f"Current user: {request.user.username if request.user.is_authenticated else 'Guest'}", style['Normal']))
    #story.append(Paragraph("____________________________________________________________________", headerStyle))
    doc.build(story)
    pdf_value = buffer.getvalue()
    buffer.close()
    response.write(pdf_value)
    return response
'''

def pdfSingleInvoice(request,pk):
    invoiceData = get_object_or_404(Invoice.objects.select_related('client_premium__client', 'duedate'), pk=pk)
    client = invoiceData.client_premium.client
    # Specific Invoice Record
    queryset = Invoice.objects.select_related('client_premium__client', 'client_premium__premium', 'duedate').filter(pk=pk)
    # All invoices belinging to a client
    #queryset = Invoice.objects.select_related('client_premium__client', 'client_premium__premium').filter(client_premium__client=client)
    itemtotal = 0
    total = 0
    for obj in queryset:
        itemtotal = (obj.unit * obj.client_premium.dollar_amount)
        total += itemtotal
 
    html_string = render_to_string('weasyprint/invoice.html', 
                                   {
                                       'invoice': invoiceData, 
                                        'client': client, 
                                        'queryset': queryset, 
                                        'total': total
                                    }
    )
    #html_string = render_to_string('weasyprint/single_profile_pdf.html', {'client': client})

    
    response = HttpResponse(content_type="application/pdf")
    response["Content-Dispostition"] = f'inline; filename="{invoiceData.invoice_id}.pdf"'
    

    HTML(string=html_string).write_pdf(response, stylesheets=['invoice/templates/weasyprint/invoice.css'])
    return response


'''
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
'''