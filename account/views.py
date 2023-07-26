from datetime import date

from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import TemplateView
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from event.models import EventRecord
from eventlify.settings import BASE_URL
from registration.models import RegistrationRecord
from organizer.forms import organizerForm
from organizer.models import organizerRecord
from .forms import SignupForm, LoginForm, ResetPasswordForm, EditUserForm, EmailForm
from .tokens import account_activation_token, password_reset_token


# Create your views here.
def is_block(request, user):
    if not user.is_active and user.last_login:
        return True
    return False


def logout(request):
    auth.logout(request)
    return redirect('event:event_list')




class Login(TemplateView):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        form1 = EmailForm()
        request.session['head_name'] = 'login'
        return render(request, self.template_name, {'form': form, 'form1': form1})

    def post(self, request):
        try:
            form = LoginForm(request.POST)
            form1 = EmailForm(request.POST)
            status=''

            # Login Form
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                user = authenticate(username=email.lower(), password=password)
                u = organizerRecord.objects.filter(Email=email)
                for i in u:
                    status = i.status
                
                if user is not None:
                    if is_block(request, user):
                        raise PermissionDenied('Your Account is blocked. Please Contact Us')
                    login(request, user)
                    if 'next' in request.POST:
                        return redirect(request.POST.get('next'))
                    if status == 'unverified':
                        messages.warning(request, 'You can add event after the admin approve')

                    return redirect("event:event_list")
                else:
                    messages.error(request, "Your authentication information is incorrect. Please try again.")

            # Forget Password
            elif form1.is_valid():
                email = form1.cleaned_data['email1']
                user = User.objects.get(username=email.lower())
                if is_block(request, user):
                    raise PermissionDenied('Your Account is blocked. Please Contact Us')

                # Email Sending
                current_site = get_current_site(request)
                mail_subject = 'Password Reset link of your eventlify Account.'
                message = render_to_string('forget-password.txt', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': password_reset_token.make_token(user),
                    'email': settings.CONTACT_EMAIL,
                    'number': settings.CONTACT_NUMBER
                })
                email = EmailMessage(mail_subject, message, to=[user.email])
                email.send()

                messages.success(request, 'Password reset link has been sent to your registered E-mail Address')
                return redirect('event:event_list')
            else:
                messages.warning(request, 'Invalid Input. Please try again')

        except ObjectDoesNotExist:
            messages.error(request, 'Invalid Inputs. Please try again')
        except PermissionDenied as e:
            messages.error(request, e)
            return redirect('event:event_list')
        except Exception as e:
            messages.error(request, (str(e) + '. Please Contact Us'))

        form = LoginForm()
        form1 = EmailForm()
        return render(request, self.template_name, {'form': form, 'form1': form1})
    
    
# noinspection PyBroadException

class Signup(TemplateView):
    template_name = 'signup.html'

    def get(self, request):
        # Render the signup form
        form = SignupForm()
        return render(request, self.template_name, {'form1': form})

    def post(self, request):
        try:
            form = SignupForm(request.POST)
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email'].lower()
                password = form.cleaned_data['password']
                try:
                    user = User.objects.get(username=email)
                    if is_block(request, user):
                        raise PermissionDenied('Your Account is blocked. Please Contact Us')
                    user.first_name = first_name
                    user.last_name = last_name
                    user.set_password(password)
                    user.save()
                    print('account created')
                except ObjectDoesNotExist:
                    user = User.objects.create(username=email, email=email, password=password, first_name=first_name,
                                               last_name=last_name, is_active=False,is_staff=False)
                    print('account created')
                    

                '''Begin Email Sending '''
                current_site = get_current_site(request)
                mail_subject = 'Action Required: Activate your eventlify account'
                message = render_to_string('acc_active_email.txt', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                    'email': settings.CONTACT_EMAIL,
                    'number': settings.CONTACT_NUMBER
                })
                email = EmailMessage(mail_subject, message, to=[user.email])
                email.send()
                '''End Email sending'''

                messages.success(request, 'Check your mail to complete registration')
                return redirect("account:login")
            else:
                messages.warning(request, 'Invalid Input. Please try again')
            
            return render(request, self.template_name, {'form1': form})

        except PermissionDenied as e:
            messages.error(request, e)
            return redirect('event:event_list')
        except Exception as e:
            messages.error(request, (str(e) + '. Please Contact Us'))
            return redirect("account:signup")


# noinspection PyBroadException
class Activate(TemplateView):
    template_name = 'activate.html'

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
            if account_activation_token.check_token(user, kwargs['token']):
                if is_block(request, user):
                    raise PermissionDenied('Your Account is blocked. Please Contact Us')

                form = organizerForm()
                return render(request, self.template_name, {'user': user, 'form': form})
            else:
                raise PermissionDenied('Activation link is invalid! Please SignUp Again or Contact Us')

        except PermissionDenied as e:
            messages.error(request, e)
            return redirect('event:event_list')
        except Exception as e:
            messages.error(request, (str(e) + '. Please Contact Us'))
            return redirect("account:signup")

    def post(self, request, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
            if account_activation_token.check_token(user, kwargs['token']):
                if is_block(request, user):
                    raise PermissionDenied('Your Account is blocked. Please Contact Us')

                form = organizerForm(request.POST,request.FILES)
                
                if form.is_valid():
                    temp = form.save(commit=False)
                    temp.user = user
                    temp.save()
                    user.is_active = False
                    user.save()
                    auth.login(request, user)
                    messages.success(request, 'Thank you for Registration')
                    messages.warning(request, 'You can add event after the admin approve')
                    return redirect("event:event_list")
                else:
                    messages.warning(request, 'Invalid Input')
                    return render(request, self.template_name, {'user': user, 'form': form})
            else:
                raise PermissionDenied('Activation link is invalid! Please SignUp Again or Contact Us')

        except PermissionDenied as e:
            messages.error(request, e)
            return redirect('event:event_list')
        except Exception as e:
            messages.error(request, (str(e) + '. Please Contact Us'))
            return redirect("account:signup")


# noinspection PyBroadException
class ForgetPassword(TemplateView):
    template_name = 'reset-password.html'

    def get(self, request, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
            if password_reset_token.check_token(user, kwargs['token']):
                if is_block(request, user):
                    raise PermissionDenied('Your Account is blocked. Please Contact Us')

                form = ResetPasswordForm()
                return render(request, self.template_name, {'form': form})
            else:
                raise PermissionDenied('Invalid Password Reset link!')

        except PermissionDenied as e:
            messages.error(request, e)
            return redirect('event:event_list')
        except Exception as e:
            messages.error(request, (str(e) + '. Please Contact Us'))
            return redirect("event:event_list")

    def post(self, request, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(kwargs['uidb64']))
            user = User.objects.get(pk=uid)
            if password_reset_token.check_token(user, kwargs['token']):
                if is_block(request, user):
                    raise PermissionDenied('Your Account is blocked. Please Contact Us')

                form = ResetPasswordForm(request.POST)
                if form.is_valid():
                    password = form.cleaned_data['password']
                    user.set_password(password)
                    user.is_active = True
                    user.save()
                    messages.success(request, 'Password Successfully Updated')
                    auth.login(request, user)
                    return redirect('event:event_list')
                messages.error(request, 'Invalid Password')
                return render(request, self.template_name, {'form': form})
            else:
                raise PermissionDenied('Invalid Password Reset link!')

        except PermissionDenied as e:
            messages.error(request, e)
            return redirect('event:event_list')
        except Exception as e:
            messages.error(request, (str(e) + '. Please Contact Us'))
            return redirect("event:event_list")


# noinspection PyBroadException
class ResetPassword(TemplateView):
    template_name = 'reset-password.html'

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.user)
            if user.is_active:
                form = ResetPasswordForm()
                return render(request, self.template_name, {'form': form})
        except Exception:
            messages.error(request, 'User not Found')
        return redirect('event:event_list')

    def post(self, request):
        try:
            user = User.objects.get(username=request.user)
            if user.is_active:
                form = ResetPasswordForm(request.POST)
                if form.is_valid():
                    password = form.cleaned_data['password']
                    user.set_password(password)
                    user.save()
                    messages.success(request, 'Password Updated')
                    auth.login(request, user)
                    return redirect('event:event_list')
                messages.error(request, 'Password Does not Match')
                return render(request, self.template_name, {'form': form})
        except Exception:
            messages.error(request, 'Invalid Link')
        return redirect('event:event_list')

class ConsolidatedView(TemplateView):
    template_name = 'consolidated_view.html'

    def get(self, request, *args, **kwargs):
        try:
            if request.user.is_superuser:
                if kwargs.get('c_o_e'):
                    event_list = EventRecord.objects.filter(c_o_e=kwargs['c_o_e']).order_by('-id')
                    print('aa')
                elif kwargs.get('username'):
                    user = User.objects.get(username=kwargs['username'])
                    event_list = EventRecord.objects.filter(user=user).order_by('-id')
                    print('bb')
                else:
                    event_list = EventRecord.objects.all().order_by('-id')
            elif request.user.is_staff:
                event_list = EventRecord.objects.filter(user=request.user).order_by('-id')
            else:
                organizer = organizerRecord.objects.get(user=request.user)
                event_list = RegistrationRecord.objects.filter(organizer=organizer)
            return render(request, self.template_name, {'event_list': event_list, 'now': date.today()})

        except ObjectDoesNotExist:
            messages.error(request, 'Record Not Found')
            return redirect('event:event_list')
        # except Exception as e:
        #     messages.error(request, (str(e) + '. Please Contact Us'))
        #     return redirect("event:event_list")


# noinspection PyBroadException
def superuser(request):
    if request.user.is_superuser:
        if request.method == "POST":
            try:
                form = SignupForm(request.POST)
                if form.is_valid():
                    username = form.cleaned_data['email']
                    first_name = form.cleaned_data['first_name']
                    last_name = form.cleaned_data['last_name']
                    email = form.cleaned_data['email']
                    password = form.cleaned_data['password']
                    User.objects.create_user(username=username.lower(), email=email.lower(), password=password,
                                             first_name=first_name, last_name=last_name, is_active=True, is_staff=True,)
                    messages.success(request, 'User Created')
                else:
                    messages.error(request, 'Invalid Inputs')
            except Exception:
                messages.warning(request, 'User name already exits')
        form = SignupForm()
        user = User.objects.filter(is_staff=True, is_superuser=False)
        new_user = User.objects.filter(is_staff=False, is_superuser=False)
        org_uv = organizerRecord.objects.filter(status='unverified')
        org_v = organizerRecord.objects.filter(status='verified')
        org_r = organizerRecord.objects.filter(status='rejected')
        base_url = BASE_URL

        return render(request, 'superuser.html', {'u': user, 'form': form, 'new':new_user, "unverified":org_uv,"verified":org_v,"rejected":org_r,'base':base_url})
    else:
        raise PermissionDenied


def accept_organizer(request, id):
    if request.method == 'POST':
        organizer = get_object_or_404(organizerRecord, id=id)
        organizer.status = 'verified'
        organizer.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def reject_organizer(request, id):
    print(request.method)
    
    if request.method == 'POST':
        organizer = get_object_or_404(organizerRecord, id=id)
        print(organizer.status)
        organizer.status = 'rejected'
        organizer.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def edit_user(request, username):
    try:
        u = User.objects.get(username=username)
        if request.user.is_superuser:
            if request.method == "POST":
                form = EditUserForm(request.POST, instance=u)
                if form.is_valid():
                    u.first_name = form.cleaned_data['first_name']
                    u.last_name = form.cleaned_data['last_name']
                    u.email = form.cleaned_data['email']
                    new_password = form.cleaned_data['password']
                    u.set_password(new_password)
                    u.save(update_fields=['username', 'password', 'first_name', 'last_name', 'email'])
                    messages.success(request, 'Updated')
                else:
                    messages.info(request, 'Invalid Input')
            form = EditUserForm(instance=u)
            return render(request, 'edit_user.html', {'form': form})
        else:
            raise PermissionDenied
    except PermissionDenied:
        messages.error(request, 'Edit not allowed!!!')
    except ObjectDoesNotExist:
        messages.error(request, 'User does not exist !!!')
    return redirect('superuser')


def del_user(request, username):
    try:
        u = User.objects.get(username=username)
        if not u.is_superuser and request.user.is_superuser:
            u.delete()
            messages.success(request, "The user is deleted")
        else:
            messages.warning(request, 'Invalid Response')
    except ObjectDoesNotExist:
        messages.error(request, "User does not exist")
        return render(request, 'superuser.html')
    except Exception as e:
        return render(request, 'superuser.html', {'err': e})
    return redirect('superuser')
