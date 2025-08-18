from django.views.generic import View
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Client, ClientIdentification, Premium, PremiumType, StatusType, Invoices

from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic.edit import FormMixin

from django.views.decorators.http import require_http_methods
from invoice.forms import ClientForm, PremiumForm, PremiumTypeForm, InvoiceForm
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy

from django_htmx.http import HttpResponseClientRefresh

from datetime import date

# REPORT LAB
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch
from django.http import HttpResponse, FileResponse
from io import BytesIO


#@login_required
def index(request):
    return render(request, 'invoice.html')

class adminCheckView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponse("Welcome, Superuser!")
        else:
            return HttpResponse("You are not a superuser.")

def invoice(request):
    invoices = Invoices.objects.all()
    form = InvoiceForm()
    context = {
        'invoices': invoices,
        'form': form,
    }
    return render(request, 'invoice.html', context)


class InvoiceListView(generic.ListView):
    model = Invoices
    paginate_by = 2


class InvoiceDetailView(generic.DetailView):
    model = Invoices
    template_name = 'invoice/partials/invoice_form_partial.html' # Render only the form

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['form'] = InvoiceForm(instance=self.object)
            return context


class InvoiceUpdateView(generic.UpdateView):
    model = Invoices
    form_class = InvoiceForm
    template_name = 'invoice/partials/invoice_form_partial.html'
    success_url = reverse_lazy('invoice:invoice')  # Or use get_success_url()

    def form_valid(self, form):
        # Process the form data (e.g., save to database)
        form.save()

        # Check if it's an HTMX request
        if self.request.headers.get('HX-Request'):
            return HttpResponseClientRefresh()
        else:
            return super().form_valid(form)





class adminCheckView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return HttpResponse("Welcome, Superuser!")
        else:
            return HttpResponse("You are not a superuser.")

def clients(request):
    clients = Client.objects.all()
    form = ClientForm()
    context = {
        'clients': clients,
        'form': form,
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

#   Premium Types
def premiumtypes(request):
    premiumtypes = PremiumType.objects.all()
    form = PremiumTypeForm()
    context = {
        'premiumtypes': premiumtypes,
        'form': form,
    }
    return render(request, 'premiumtypes.html', context)


class PremiumTypeListView(generic.ListView):
    model = PremiumType
    paginate_by = 2


class PremiumTypeDetailView(generic.DetailView):
    model = PremiumType
    template_name = 'invoice/partials/premiumtype_form_partial.html' # Render only the form

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['form'] = PremiumTypeForm(instance=self.object)
            return context


class PremiumTypeUpdateView(generic.UpdateView):
    model = PremiumType
    form_class = PremiumTypeForm
    template_name = 'invoice/partials/premiumtype_form_partial.html'
    success_url = reverse_lazy('invoice:premiumtypes')  # Or use get_success_url()

    def form_valid(self, form):
        # Process the form data (e.g., save to database)
        form.save()

        # Check if it's an HTMX request
        if self.request.headers.get('HX-Request'):
            return HttpResponseClientRefresh()
        else:
            return super().form_valid(form)




from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame, BaseDocTemplate, PageTemplate, NextPageTemplate, PageBreak, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib import colors


def generate_pdf_report(request, pk):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # database data
    client = Client.objects.get(pk = pk)

    all_invoices_by_client = Invoices.objects.filter(Premium_ID__Client_ID__first_name="Tyson").values()
    clientInvoices = Invoices.objects.select_related('Premium_ID__Client_ID')
    #print(clientInvoices.values())
    #obj = clientInvoices.first()

    allInvoices = Invoices.objects.all()
    print(allInvoices.values())
    for inv in allInvoices:
        print(inv.premium_set.all())

    

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

    subtotal = 0.00
    '''
    queryset = Invoices.objects.filter(Premium_ID__Client_ID__first_name="Tyson")
    queryData = [['Description', 'Quantity', 'Amount', 'Total Due']]
    for obj in queryset:
        queryData.append([(obj.first_name + " " + obj.last_name), obj.address, obj.city, obj.state])
        subtotal+= 1
    '''
    queryset = Client.objects.all()
    queryData = [['Description', 'Quantity', 'Amount', 'Total Due']]
    for obj in queryset:
        queryData.append([(obj.first_name + " " + obj.last_name), obj.address, obj.city, obj.state])
        subtotal+= 1
    
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
    story.append(Paragraph(("Invoice Date: " +  str(date.today()) + "  Inv No: " + client.first_name), rightHeaderStyle))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Due Date: Monthly", rightHeaderStyle))
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

# REPORT LAB
def pdfAuthors(request):
    #   HTTPResponse is used for creating new files, FileResponse is for serving premade files stored on a disk
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="hello.pdf"'
    buffer = BytesIO()
    #   canvas styling
    p = canvas.Canvas(buffer, pagesize=letter)
    PAGE_WIDTH, PAGE_HEIGHT = letter      #   Setting page width and height as variables for later use
    headerSize = 16             #   defining header size and style
    headerStyle = "Courier"
    bodySize = 16
    bodyStyle = "Courier"
    p.setFont(headerStyle, headerSize)
    p.setFillColorRGB(0.14, 0.59, 0.74)

    p.drawString(PAGE_WIDTH/12, PAGE_HEIGHT/12, "Appalachian Agency for Senior Citizens")
    p.drawString(PAGE_WIDTH/10, PAGE_HEIGHT/10, "P.O. Box 765")
    p.setFont(bodyStyle, bodySize)
    p.setFillColorRGB(0, 0, 0)

    #data collection
    clients = Client.objects.all()
    print(clients)
    positionY = 700
    for client in clients:
        p.drawString(60, positionY, client.first_name + " " + client.last_name)
        positionY -= 25
    
    # saving the file
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
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