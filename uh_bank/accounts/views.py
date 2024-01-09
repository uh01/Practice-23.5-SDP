from django.shortcuts import render
from django.views.generic import FormView
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.contrib.auth.forms import SetPasswordForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class UserRegistrationView(FormView):
    template_name = 'accounts/user_signin.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('profile')
    
    def form_valid(self,form):
        print(form.cleaned_data)
        user = form.save()
        login(self.request, user)
        print(user)
        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = 'accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')


class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')


class UserBankAccountUpdateView(LoginRequiredMixin,View):
    template_name = 'accounts/user_profile.html'

    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
    

def password_change_email(user, subject, template):
        message = render_to_string(template, {
            'user' : user,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


class UserPasswordChangeView(LoginRequiredMixin, FormView):
    template_name = 'accounts/user_profile.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.save()
        password_change_email(self.request.user, "Password Change Message", "accounts/password_update_email.html")
        messages.success(self.request, 'Password Updated Successfully')
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    