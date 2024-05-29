from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout, authenticate
from django.views import View
from kavenegar import *
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Review, Customer, OTP
from products.models import Product
from .forms import ReviewForm, UserCreationForm, UserLoginForm, UserCreationForm, CustomerRegistrationForm, RegisterForm
from django.urls import reverse_lazy
from . import kaveSMS
from .kaveSMS import get_random_otp
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages


# Review Creation View :
class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'

    def form_valid(self, form):
        form.instance.customer = self.request.user.customer
        form.instance.product = get_object_or_404(Product, id=self.kwargs['product_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_detail', kwargs={'pk': self.kwargs['product_id']})


# send OTP for login or Registering :
def register_view(request):
    
    form = RegisterForm
    if request.method == "POST":
        try:
            if "mobile" in request.POST:
                mobile = request.POST.get('mobile')
                user = Customer.objects.get(mobile=mobile)
                # send otp
                otp = get_random_otp()
                # helper.send_otp(mobile, otp)
                kaveSMS.send_otp_soap(mobile, otp)
                print('OTP: ', otp)
                # save otp
                print(otp)
                user.otp = otp
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse('verify'))

        except Customer.DoesNotExist:
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                # send otp
                otp = get_random_otp()
                # helper.send_otp(mobile, otp)
                kaveSMS.send_otp_soap(mobile, otp)
                print('OTP: ', otp)
                # save otp
                print(otp)
                user.otp = otp
                user.is_active = False
                user.save()
                request.session['user_mobile'] = user.mobile
                return HttpResponseRedirect(reverse('verify'))
    return render(request, 'custom_loggin/register.html', {'form': form})


# check OTP for redirecting to dashboard or retry for loggin if inccorect :
def verify(request):
    
    try:
        mobile = request.session.get('user_mobile')
        user = Customer.objects.get(mobile = mobile)

        if request.method == "POST":

            # check otp expiration
            if not kaveSMS.check_otp_expiration(user.mobile):
                messages.error(request, "زمان رمز یکبار مصرف به \ایان رسیده است دوباره امتحان کنید.")
                return HttpResponseRedirect(reverse('register_view'))

            if user.otp != int(request.POST.get('otp')):
                messages.error(request, "کد اشتباه وارد شد.")
                return HttpResponseRedirect(reverse('verify'))

            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('dashboard'))

        return render(request, 'custom_loggin/verify.html', {'mobile': mobile})

    except Customer.DoesNotExist:
        messages.error(request, "خطا دوباره امتحان کنید.")
        return HttpResponseRedirect(reverse('register_view'))
    
    
# Login View:
class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'custom_loggin/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        return render(request, 'custom_loggin/login.html', {'form': form})


# Logout View:
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
    
# Register View for username and password
class RegisterUserView(View):
    def get(self, request):
        user_form = UserCreationForm()
        customer_form = CustomerRegistrationForm()
        return render(request, 'custom_loggin/register_user.html', {'user_form': user_form, 'customer_form': customer_form})

    def post(self, request):
        user_form = UserCreationForm(request.POST)
        customer_form = CustomerRegistrationForm(request.POST)
        if user_form.is_valid() and customer_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password1'])
            user.save()

            customer = customer_form.save(commit=False)
            customer.user = user
            customer.save()

            user = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')

            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        return render(request, 'custom_loggin/register_user.html', {'user_form': user_form, 'customer_form': customer_form})