from datetime import date

from django.contrib import messages
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from organizer.models import organizerRecord
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect


from registration.models import RegistrationRecord
from .forms import AnswerForm, EventForm,ClientForm
from .models import Answer, EventRecord,Client
from eventlify.settings import BASE_URL



def createform(request,*args, **kwargs):
    if(request.method == "POST"):
        form = ClientForm(request.POST)
        obj = EventRecord.objects.get(slug=kwargs['slug'])
        if form.is_valid():
            temp = form.save(commit=False)
            print("**********************")
            
            # if(temp.label.lower() == 'email'):
                
            
            print(temp.label=='email')
            print("**********************")
            temp.organizer = request.user
            temp.event = obj
            temp.save()
            
            messages.success(request, 'Submitted Successfully')
            context = {"form": temp}
            return render(request, "form/contact.html",context)
    
    else:
        try:
            obj = EventRecord.objects.get(slug=kwargs['slug'])
            form = ClientForm()
            context = {'form': form,'slug':obj.slug}
            return render(request, "form/form.html", context)
        except Exception:
            return redirect('event:event_list')
        


def answerform(request,*args, **kwargs):
    if(request.method == "POST"):
        form = AnswerForm(request.POST)
        obj = EventRecord.objects.get(slug=kwargs['slug'])
        if form.is_valid():
            temp = form.save(commit=False)
            temp.user = request.user
            temp.event = obj
            temp.save()
            messages.success(request, 'Submitted Successfully')
            context = {"contact": temp}
            return render(request, "form/contact.html",context)
    
    else:
        try:
            obj = EventRecord.objects.get(slug=kwargs['slug'])
            form = AnswerForm()
            context = {'form': form,'slug':obj.slug}
            return render(request, "form/form.html", context)
        except Exception:
            return redirect('event:event_list')
        

def updateform(request, *args, **kwargs):
    obj = get_object_or_404(EventRecord, slug=kwargs['slug'])
    clt_queryset = Client.objects.filter(event=obj)
    
    if request.method == "POST":
        ClientFormSet = modelformset_factory(Client, form=ClientForm, extra=0)
        formset = ClientFormSet(request.POST, queryset=clt_queryset)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Form Updated')
            context = {"formupdate": formset}
            return render(request, "form/contact.html", context)
        else:
            messages.error(request, 'Invalid Input')
    else:
        formset = ClientForm()

    context = {'formset': formset, 'slug': obj.slug}
    return render(request, "form/form.html", context)


def showform(request, *args, **kwargs):
    obj = EventRecord.objects.get(slug=kwargs['slug'])
    clt = Client.objects.filter(event=obj)
    
    if clt:
        ClientFormSet = modelformset_factory(Client, form=ClientForm, extra=0)
        formset = ClientFormSet(queryset=clt)
    else:
        formset = ClientForm()
    
    context = {'formset': formset, 'slug': obj.slug, 'client': clt}
    return render(request, "form/index.html", context)

    

# Create your views here.
class EventListView(TemplateView):
    template_name = 'event-list.html'

    def get(self, request, *args, **kwargs):
        request.session['head_name'] = 'event'
        event_list = EventRecord.objects.all().order_by('-event_start_date')
        return render(request, self.template_name, {'event_list': event_list})


# noinspection PyBroadException
class EventDetail(TemplateView):
    template_name = 'event_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            owner = False
            registered = True
            obj = EventRecord.objects.get(slug=kwargs['slug'])
            base_url = BASE_URL
            
            if obj.user == request.user or request.user.is_superuser:
                owner = True
            else:
                try:
                    RegistrationRecord.objects.get(user=request.user, event=obj)
                except Exception:
                    registered = False
            return render(request, self.template_name,
                          {'obj': obj, 'owner': owner, 'registered': registered, 'now': date.today(),'base':base_url})
        except ObjectDoesNotExist:
            messages.error(request, 'Event Not found')
            return redirect('event:event_list')


    # def post(self, request):
    #     if True:
    #         if request.user.is_staff:
    #             form = EventForm(request.POST, request.FILES)
    #             if form.is_valid():
    #                 temp = form.save(commit=False)
    #                 temp.user = request.user
    #                 form.save()
    #                 messages.success(request, 'Event Added')
    #                 return redirect('event:event_detail', slug=temp.slug)
    #             else:
    #                 messages.error(request, 'Invalid Input')
    #         else:
    #             raise PermissionDenied
    #         return render(request, self.template_name, {'form': form,'base':BASE_URL})
    
# noinspection PyBroadException
class AddEvent(TemplateView):
    template_name = 'add_update_event.html'
    def get(self, request, *args, **kwargs):
        status = ''
        
        st = organizerRecord.objects.filter(user=request.user)
        for i in st:
            status = i.status
        if status == 'verified':
            try:
                if request.user.is_staff:
                    form = EventForm()
                else:
                    raise PermissionDenied
                return render(request, self.template_name, {'form': form})
            except PermissionDenied:
                messages.error(request, 'Permission Denied')
                return redirect('event:event_list')
        else:
            messages.warning(request, "Your account is not verified.please wait until it verify")
            return redirect('event:event_list')

    def post(self, request):
        try:
            if request.user.is_staff:
                form = EventForm(request.POST, request.FILES)
                if form.is_valid():
                    temp = form.save(commit=False)
                    temp.user = request.user
                    temp.save()
                    messages.success(request, 'Event Added')
                    return redirect('event:event_form',temp.slug)
                else:
                    messages.error(request, 'Invalid Input')
            else:
                raise PermissionDenied
            return render(request, self.template_name, {'form': form,'base':BASE_URL})
        except Exception:
            messages.error(request, 'Permission Denied')
            return redirect('event:event_list')


# noinspection PyBroadException
class UpdateEvent(TemplateView):
    template_name = 'add_update_event.html'

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_staff or request.user.is_superuser:
                obj = EventRecord.objects.get(slug=kwargs['slug'])
                if obj.user == request.user or request.user.is_superuser:
                    form = EventForm(instance=obj)
                else:
                    raise PermissionDenied
            else:
                raise PermissionDenied
            return render(request, self.template_name, {'form': form})
        except Exception:
            messages.error(request, 'Permission Denied')
            return redirect('event:event_list')

    def post(self, request, **kwargs):
        try:
            obj = EventRecord.objects.get(slug=kwargs['slug'])
            f = obj.fees
            if obj.user == request.user or request.user.is_superuser:
                form = EventForm(request.POST, request.FILES, instance=obj)
                if form.is_valid():
                    fee = form.cleaned_data['fees']
                    diff = fee - f
                    if diff != 0:
                        organizer_list = RegistrationRecord.objects.filter(event=obj)
                        for organizer in organizer_list:
                            organizer.balance += diff
                            organizer.save(update_fields=['balance'])
                    form.save()
                    messages.success(request, 'Event Updated')
                    # return redirect('event:event_detail', kwargs['slug'])
                    return redirect('event:event_form',kwargs['slug'])
                else:
                    messages.error(request, 'Invalid Input')
                return render(request, self.template_name, {'form': form})
            else:
                
                raise PermissionDenied
        except Exception:
            messages.error(request, 'Permission Denied')
            return redirect('event:event_list')


class DeleteEvent(TemplateView):

    def get(self, request, *args, **kwargs):
        try:
            obj = EventRecord.objects.get(slug=kwargs['slug'])
            if str(obj.timestamp) == kwargs['timestamp'] and (obj.user == request.user or request.user.is_superuser):
                if obj.registered_organizer > 0:
                    raise PermissionDenied('organizer Registered, You can not delete this event.')
                obj.delete()
                messages.success(request, 'Event Deleted')
            else:
                raise PermissionDenied('Permission Denied')
        except ObjectDoesNotExist:
            messages.error(request, 'Event Not found')
            return redirect('event:event_list')
        except PermissionDenied as msg:
            messages.warning(request, msg)
            return redirect('account:consolidated_view_all')
