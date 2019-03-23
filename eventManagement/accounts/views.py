from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate
from accounts.forms import (
    RegistrationForm,
    EditProfileForm
)
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Interest_Model
from .forms import UserProfileForm
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.views.generic import UpdateView
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import Http404


# Create your views here.
@login_required(login_url="/accounts/login")
def home(request):
    return render(request, 'accounts/home.html')


def signup_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Circlr account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'accounts/email_confirm.html')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def signup_detailsview(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if profile_form.is_valid():
            profile_form.save()
            interest_var = request.POST.get('interests')
            interest_var = interest_var.lower().replace(",", " ")
            interest_var = interest_var.split()
            for var in interest_var:
                a = User.objects.get(username=request.user.username)
                Interest_Model.objects.create(username=a, interest=var)
            return redirect('accounts:home')
        else:
            messages.error(request, ('Please correct the error below'))
    else:
        profile_form = UserProfileForm(instance=request.user.userprofile)
    return render(request, 'accounts/details.html', {'profile_form': profile_form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('accounts:home')
        else:
            form = AuthenticationForm()
        return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    # if request.method == 'POST':
    logout(request)
    return redirect('accounts:home')


@login_required(login_url="/accounts/login")
def settings_view(request, username):
    if request.user == User.objects.get(username=username):
        return render(request, 'accounts/settings.html')
    else:
        raise Http404


@csrf_exempt
@login_required(login_url="/accounts/login")
def delete_account(request):
    confirm = request.POST.get("confirm")
    print(confirm)
    if confirm == "ok":
        print("Confirm is ok")
        u = User.objects.get(username=request.user.username)
        u.delete()
        logout(request)
    return redirect('accounts:home')


@login_required(login_url="/accounts/login")
def delete_view(request):
    return render(request, 'accounts/delete_confirm.html')


@login_required(login_url="/accounts/login")
def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    interests = Interest_Model.objects.filter(username=user)
    editable = False
    if request.user.is_authenticated and request.user == user:
        editable = True
    interestlist = []
    for i in interests:
        interestlist.append(i.interest)

    args = {'user': user, 'editable': editable, 'interestlist': interestlist}
    return render(request, 'accounts/profile.html', args)


@login_required(login_url="/accounts/login")
def edit_profile(request, username):
    user = User.objects.get(username=username)
    inters = Interest_Model.objects.filter(username=user)
    interest_list = []
    for i in inters:
        interest_list.append(i.interest)
    if request.user.is_authenticated and request.user == user:
        if request.method == 'POST':
            user_form = EditProfileForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                to_delete = Interest_Model.objects.filter(username=user)
                if to_delete.exists():
                    to_delete.delete()
                interest_var = request.POST.get('interests')
                interest_var = interest_var.lower().replace(",", " ")
                interest_var = interest_var.split()
                for var in interest_var:
                    a = User.objects.get(username=request.user.username)
                    Interest_Model.objects.create(username=a, interest=var)
                messages.success(request, ('Your profile was successfully updated!'))
                return redirect(reverse('accounts:profile', args=[request.user]))
            else:
                messages.error(request, ('Please correct the error below.'))
        else:
            user_form = EditProfileForm(instance=request.user)
            profile_form = UserProfileForm(instance=request.user.userprofile)
        args = {'user_form': user_form, 'profile_form': profile_form, 'interest_list': interest_list}
        return render(request, 'accounts/edit_profile.html', args)


@login_required(login_url="/accounts/login")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts')
        else:
            return redirect('/accounts/change-password')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.emailconfirm.email_confirmed = True
        user.save()
        login(request, user)
        # return redirect('home')
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('accounts:details')
    else:
        return HttpResponse('Activation link is invalid!')
