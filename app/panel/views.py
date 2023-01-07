from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.views import View
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import reverse


from .forms import ZarejestrujForm


def index(request):
    return render(request, 'index.html', {})

class LoginView(auth_views.LoginView):
    template_name = 'auth/login.html'


class LogoutView(auth_views.LogoutView):
    template_name = 'auth/logged_out.html'


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'auth/password_change_form.html'


class PasswordChangeDoneView(auth_views.PasswordChangeDoneView):
    template_name = 'auth/password_change_done.html'

class Zarejestruj(View):
    template_name = 'auth/zarejestruj.html'
    form = ZarejestrujForm

    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, template_name=self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = False
            user.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        return render(request, template_name=self.template_name, context={'form': form})


