from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token


def home(request):
    """Here should be options login and registration for unauthorized user, and feed for authorized user"""
    return redirect('login')


@unauthenticated_user
def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if user.first_name and user.last_name:
                    return redirect("feed")
                else:
                    return redirect("edit_profile")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, 'app/login.html', {'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, "You've been logged out successfully")
    return redirect('login')


@unauthenticated_user
def registration_page(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            form.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('login')
    context = {'form': form}
    return render(request, 'app/registration.html', context)


def activateEmail(request, user, to_email):
    mail_subject = 'Activate your user account.'
    message = render_to_string('app/template_activate_account.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, "Please, check the email and follow the instructions to activate your account")
    else:
        messages.error(request, f'Problem sending confirmation email to {to_email}, check if you typed it correctly.')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Thank you for confirming the email address. Now you can login to your account.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid!')

    return redirect('login')


@login_required(login_url='login')
def feed(request):
    return render(request, 'app/feed.html')


@login_required(login_url='login')
def my_profile(request):
    return render(request, 'app/my_profile.html')


@login_required(login_url='login')
def edit_profile(request):
    user = request.user
    form = EditProfileForm(instance=user)
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'The information in your profile has been successfully changed')
            return redirect('my_profile')
    context = {'form': form}
    return render(request, 'app/edit_profile.html', context)


@login_required(login_url='login')
def create_post(request):
    return render(request, 'app/new_post.html')


@login_required(login_url='login')
def view_users_profile(request):
    return render(request, 'app/users_profile.html')
