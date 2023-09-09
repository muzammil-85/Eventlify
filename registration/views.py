from email.mime.image import MIMEImage
import os
from io import BytesIO
from xhtml2pdf import pisa
import io
from reportlab.lib.utils import flatten, open_for_read
# from html2image import Html2Image

import xlwt
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template, render_to_string
from django.utils import timezone
from django.views.generic import TemplateView
import razorpay
from eventlify import settings

from event.forms import AnswerForm
from event.models import Answer, Client, EventRecord
from organizer.models import organizerRecord
from .forms import TransactionForm
from .models import PaymentRecord, RegistrationRecord,Answer
from organizer.models import organizerRecord
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from datetime import date

from django.views.decorators.csrf import csrf_exempt


class RegisterEvent(TemplateView):
    template_name = 'organiser_dynamic.html'
    qstn = []
    client_data = {}  # Dictionary to store client data
    count = 1
    
    def get(self, request, *args, **kwargs):
        try:
            obj = EventRecord.objects.get(slug=kwargs['slug'])
            organizer = organizerRecord.objects.get(user=obj.user)
        except EventRecord.DoesNotExist:
            messages.error(request, 'Event not found')
            return redirect('home')
        except organizerRecord.DoesNotExist:
            messages.info(request, 'Fill your personal information before registration')
            return redirect('home')
        
        if not request.user.is_authenticated or (not request.user.is_staff and not request.user.is_superuser):
            t = date.today()
            if obj.registration_open and (obj.registration_start <= t) and (t <= obj.registration_end):
                try:
                    client = Answer.objects.get(email=None)
                    messages.warning(request, 'You are already registered for this event.')
                except Answer.DoesNotExist:
                    form = Client.objects.filter(event=obj) 
                    context = self.get_context_data(form=form, event=obj, organizer=organizer)
                    return self.render_to_response(context)
            else:
                messages.info(request, 'Registration Closed/Does not Start')
        else:
            raise PermissionDenied
        return redirect('event:event_detail', kwargs['slug'])

    def post(self, request, *args, **kwargs):
        try:
            obj = EventRecord.objects.get(slug=kwargs['slug'])
            clt = Client.objects.filter(event=obj)
            organizer = organizerRecord.objects.get(user=obj.user)
            
        except EventRecord.DoesNotExist:
            messages.error(request, 'Event not found')
            return redirect('home')
        except Client.DoesNotExist:
            messages.info(request, 'error !!.please contact us')
            return redirect('home')
        
        if not request.user.is_authenticated or (not request.user.is_staff and not request.user.is_superuser):
            t = date.today()
            if obj.registration_open and (obj.registration_start <= t) and (t <= obj.registration_end):
                
                for i in clt:
                    if i.label:
                        if i.label not in self.qstn:
                            self.qstn.append(i.label)
                
                # Assuming you have a Client model with fields: name, email, and other necessary fields
                

                for input_name in self.qstn:
                    # Check if the input_name exists in request.POST
                    if input_name in request.POST:
                        self.client_data[input_name] = request.POST.get(input_name)
                # Create the Client instance and populate it with client_data
                client = Answer()
                for field_name, value in self.client_data.items():
                    setattr(client, field_name, value)
                id = request.POST.get("label_id")
                question = Client.objects.get(id=id)
                client.question = question
                client.response = request.POST.get(question.label)
                client.event = obj
                client.save()
                current_site = get_current_site(request)
                ticket(request,obj.slug) #calling ticket funtion
                mail_subject = f'We are happy to see you at our event {obj.event_title}.'
                message = render_to_string('registration_email.txt', {
                    'domain': current_site.domain,
                    'event': obj,
                    'email': settings.EMAIL_HOST_USER,
                })
                email = EmailMessage(mail_subject, message, to=[client.email])
                if self.count == 1:
                    self.count = 0
                    
                    if obj.event_booked < obj.no_of_tickets:
                        obj.event_booked += 1
                        RegistrationRecord.objects.create(amount=obj.fees, answer=client, event=obj,
                                                          organizer=organizer)
                        email.send()
                        print(f"email send")
                        obj.save(update_fields=['event_booked'])
                        msg = f'Successfully registered for {obj.event_title}.please check your mail.'
                        messages.success(request, msg)
                return HttpResponse("registered successfully.Please check your mail.")
            else:
                messages.info(request, 'Registration Closed/Does not Start')
        else:
            raise PermissionDenied
            return redirect('event:event_detail', kwargs['slug'])



# noinspection PyBroadException
class RegistrationDetail(TemplateView):
    template_name = 'registration_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            obj = RegistrationRecord.objects.get(registration_id=kwargs['registration_id'])
            if request.user.is_superuser or request.user == obj.event.user:
                form = TransactionForm()
                return render(request, self.template_name, {'obj': obj, 'form': form, 'staff': True})
            organizer = organizerRecord.objects.get(user=request.user)
            if organizer == obj.organizer:
                return render(request, self.template_name, {'obj': obj, 'staff': False})
            raise PermissionDenied
        except Exception:
            messages.error(request, 'You Does not Permission')
            return redirect('home')

    def post(self, request, **kwargs):
        try:
            obj = RegistrationRecord.objects.get(registration_id=kwargs['registration_id'])
            if request.user.is_superuser or request.user == obj.event.user:
                form = TransactionForm(request.POST)
                if form.is_valid():
                    temp = form.save(commit=False)
                    temp.registration_id = obj.id
                    temp.user = request.user
                    obj.amount += temp.amount
                    temp.save()
                    obj.save(update_fields=['amount'])
                    obj.transaction_id.add(temp)
                    messages.success(request, 'Successfully Update')
                    return redirect('registration:registration_detail', kwargs['registration_id'])
                else:
                    messages.error(request, 'Invalid Inputs')
                    return render(request, self.template_name, {'obj': obj, 'form': form, 'staff': True})
            else:
                raise PermissionDenied
        except PermissionDenied:
            messages.error(request, 'You Does not Permission')
            return redirect('home')
        except Exception:
            messages.error(request, 'Error, Contact to US')
            return redirect('home')


# noinspection PyBroadException
class RegisterParticipantList(TemplateView):
    template_name = 'participant_list.html' 

    def get(self, request, *args, **kwargs):
        # try:
            event = EventRecord.objects.get(slug=kwargs['slug'])
            # question = Client
            # participant = Answer.objects.filter(event=event)
            # print(participant)
            # participant = ''
            if request.user.is_superuser or request.user == event.user:
                obj = RegistrationRecord.objects.filter(event=event.id)
                organizer = organizerRecord.objects.get(user=event.user)
                clt = Client.objects.filter(event=event)
                form = Answer.objects.filter(question=clt)
                # email use cheyth filter cheyyanam athinn payment id okke payment tablelil save cheyyanam
                context = self.get_context_data(form=form, event=obj, organizer=organizer)
                return self.render_to_response(context)
                # return render(request, self.template_name, {'obj': obj,'participant':participant})
            raise PermissionDenied
        # except Exception:
        #     messages.error(request, 'You Does not Permission')
        #     return redirect('home')


class RegistrationReport(TemplateView):
    template_name = 'report.html'

    def get(self, request, *args, **kwargs):
        try:
            event = EventRecord.objects.get(slug=kwargs['slug'])
            if request.user.is_superuser or request.user == event.user:
                organizer_list = RegistrationRecord.objects.filter(event=event)
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = "attachment; filename=Registration_Report_{}.xls".format(event.slug)
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet(event.slug)

                # Define style for header and data cells
                header_style = xlwt.easyxf('font: bold on; pattern: pattern solid, fore_colour light_blue;'
                                           'align: vert centre, horiz center; borders: left thin, right thin, top thin, bottom thin')
                data_style = xlwt.easyxf('align: vert centre, horiz left; borders: left thin, right thin, top thin, bottom thin')

                # Sheet header, first row
                ws.write_merge(0, 0, 0, 6, 'Eventlify', header_style)

                ws.write(2, 0, 'Event Code', header_style)
                ws.write(2, 1, event.slug, data_style)
                ws.write(2, 2, 'Event Name', header_style)
                ws.write_merge(2, 2, 3, 6, event.event_title, data_style)

                ws.write(3, 0, 'Event Date', header_style)
                ws.write(3, 1, event.event_start_date.strftime('%b %d, %Y'), data_style)
                ws.write(3, 2, 'Event Fees', header_style)
                ws.write(3, 3, event.fees, data_style)

                row_num = 5
                columns = ['S. No.', 'Registration Id', 'Name', 'Amount', 'Date']
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], header_style)
                    # Set column widths
                    ws.col(col_num).width = 5000

                # Sheet body, remaining rows
                for organizer in organizer_list:
                    row_num += 1
                    ws.write(row_num, 0, row_num - 5, data_style)
                    ws.write(row_num, 1, organizer.id, data_style)
                    ws.write(row_num, 2, organizer.organizer.user.get_full_name(), data_style)
                    ws.write(row_num, 3, organizer.amount, data_style)
                    ws.write(row_num, 4, organizer.timestamp.strftime('%b %d, %Y'), data_style)

                ws.write_merge(row_num + 2, row_num + 2, 0, 6, 'Printed on ' + str(timezone.now()) + ' (UTC)', data_style)

                # Set row height for the header and data rows
                for row_idx in range(5, row_num + 1):
                    ws.row(row_idx).height_mismatch = True
                    ws.row(row_idx).height = 300

                wb.save(response)
                return response
            raise PermissionDenied
        except PermissionDenied:
            messages.error(request, 'You do not have permission to access this report.')
            return redirect('home')
        except Exception:
            messages.error(request, 'Something went wrong.')
            return redirect('home')


class TransactionReport(TemplateView):
    template_name = 'report.html'

    def get(self, request, *args, **kwargs):
        try:
            event = EventRecord.objects.get(slug=kwargs['slug'])
            if request.user.is_superuser or request.user == event.user:
                organizer_list = RegistrationRecord.objects.filter(event=event)
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = "attachment; filename=Transaction_Report_{}.xls".format(event.slug)
                wb = xlwt.Workbook(encoding='utf-8')
                ws = wb.add_sheet(event.slug)

                # Define style for header and data cells
                header_style = xlwt.easyxf('font: bold on; pattern: pattern solid, fore_colour light_blue;'
                                           'align: vert centre, horiz center; borders: left thin, right thin, top thin, bottom thin')
                data_style = xlwt.easyxf('align: vert centre, horiz left; borders: left thin, right thin, top thin, bottom thin')

                # Sheet header, first row
                ws.write_merge(0, 0, 2, 4, 'Eventlify', header_style)

                ws.write(2, 0, 'Event Code', header_style)
                ws.write(2, 1, event.slug, data_style)
                ws.write(2, 2, 'Event Name', header_style)
                ws.write_merge(2, 2, 3, 6, event.event_title, data_style)

                ws.write(3, 0, 'Event Date', header_style)
                ws.write(3, 1, event.event_start_date.strftime('%b %d, %Y'), data_style)
                ws.write(3, 2, 'Event Fees', header_style)
                ws.write(3, 3, event.fees, data_style)

                row_num = 5
                columns = ['S. No.', 'Receipt No.', 'Name', 'Amount', 'Date', 'User']
                for col_num in range(len(columns)):
                    ws.write(row_num, col_num, columns[col_num], header_style)
                    # Set column widths
                    ws.col(col_num).width = 5000

                # Sheet body, remaining rows
                for organizer in organizer_list:
                    for s in organizer.transaction_id.all():
                        row_num += 1
                        ws.write(row_num, 0, row_num - 5, data_style)
                        ws.write(row_num, 1, organizer.id, data_style)
                        ws.write(row_num, 2, organizer.organizer.user.get_full_name(), data_style)
                        ws.write(row_num, 3, s.amount, data_style)
                        ws.write(row_num, 4, s.timestamp.strftime('%b %d, %Y'), data_style)
                        ws.write(row_num, 5, s.user.username, data_style)

                ws.write_merge(row_num + 2, row_num + 2, 0, 6, 'Printed on ' + str(timezone.now()) + ' (UTC)', data_style)

                # Set row height for the header and data rows
                for row_idx in range(5, row_num + 1):
                    ws.row(row_idx).height_mismatch = True
                    ws.row(row_idx).height = 300

                wb.save(response)
                return response
            raise PermissionDenied
        except PermissionDenied:
            messages.error(request, 'You do not have permission to access this report.')
            return redirect('home')
        except Exception:
            messages.error(request, 'Something went wrong.')
            return redirect('home')



# noinspection PyBroadException

class EnrollmentReport(TemplateView):
    template_name = 'report.html'

    def get(self, request, *args, **kwargs):
        try:
            event = EventRecord.objects.get(slug=kwargs['slug'])
            if request.user.is_superuser or request.user == event.user:
                if event.fees == 0:
                    organizer_list = RegistrationRecord.objects.filter(event=event)
                else:
                    organizer_list = RegistrationRecord.objects.filter(event=event, amount=event.fees)

                template = get_template('report.html')
                html = template.render({'event': event, 'organizer_list': organizer_list, 'now': timezone.now()})

                pdf_buffer = io.BytesIO()
            pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf_buffer)

            if not pdf.err:
                response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
                filename = 'Enrollment_Report_{}.pdf'.format(event.slug)
                content = "attachment; filename={}".format(filename)
                response['Content-Disposition'] = content
                return response

            return HttpResponse("Not found")
        except EventRecord.DoesNotExist:
            messages.error(request, 'Event not found')
            return redirect('home')
        except PermissionDenied:
            messages.error(request, 'You do not have permission to access this report.')
            return redirect('home')
        except Exception:
            messages.error(request, 'Something went wrong')
            return redirect('home')



def payment_view(request,**kwargs):
    
    obj = EventRecord.objects.get(slug=kwargs['slug'])
    quantity = request.GET.get('quantity', 1)  # Default quantity is 1
    amount = obj.fees*float(quantity)  # Set the amount dynamically or based on your requirements
    
    # Initialize the Razorpay client
    client = razorpay.Client(auth=("rzp_test_ed1EgEwfNU16fv", "MgBAMD5NUzQl4eIT2Wy0wMhm"))

    
    # Create the Razorpay order
    order_data = {
        'amount': amount*100,  # Amount should be in paise (Indian currency)
        'currency': 'INR',
        # Add any additional data you need, like 'receipt', 'notes', etc.
    }
    payment = client.order.create(data=order_data)
    settings.BASE_URL
    callback_url = settings.BASE_URL+'/registration/'+obj.slug+'/payment/success'
    print(callback_url)
    context = {
        'payment': payment,
        'obj':obj,
        'callback_url':callback_url,
        'qty':quantity,
        'razorpay_key': settings.RAZORPAY_API_KEY,
    }
    return render(request, 'payment.html', context)


@csrf_exempt
def payment_success_view(request,**kwargs):
    if request.method == 'POST':
        client = razorpay.Client(auth=("rzp_test_ed1EgEwfNU16fv", "MgBAMD5NUzQl4eIT2Wy0wMhm"))
        order_id = request.POST.get('razorpay_order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        check=client.payment.fetch(payment_id)
        signature = request.POST.get('razorpay_signature')
        
        obj = EventRecord.objects.get(slug=kwargs['slug'])
        organizer = organizerRecord.objects.get(Email=obj.user)
        # need to store this in table
        PaymentRecord.objects.create(order_id=order_id,payment_id=payment_id,signature=signature,organizer=organizer,event=obj,amount=obj.fees)
        print(check)
        print(payment_id)
        print(order_id)
        print(signature)
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        try:
            # Verify the payment signature
            client.utility.verify_payment_signature(params_dict)
            # Payment signature verification successful
            # Perform any required actions (e.g., update the order status)
            messages.success(request, "payment success,please fill your details")
            return redirect('registration:register_event',kwargs['slug'])
        except razorpay.errors.SignatureVerificationError as e:
            # Payment signature verification failed
            # Handle the error accordingly
            messages.error(request, "Error occur, please try again ", e)
            return redirect('home')


    # Handle GET request
    return HttpResponse("Method not allowed", status=405)


def ticket(request,slug):
    obj = EventRecord.objects.get(slug=slug)
    # obj = EventRecord.objects.get(slug='event3-20230726162216')
    base_url = settings.BASE_URL
    context = {
        'obj':obj,
        'base':base_url,
    }
    return render(request, "ticket/ticket.html",context)