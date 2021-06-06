from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse
from django.shortcuts import redirect

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import forms

from django.contrib.auth.views import LoginView

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].required = False

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None:
            self.user_cache = self.authenticate(username=username)
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def authenticate(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None


# class LoginView(CreateView):
#     model = User
#     form_class = LoginForm
#     template_name = 'registration/login.html'
#     # def get_success_url(self):
#     #     return reverse('home')


#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         # feed = Feed.objects.create(user=user, post=welcome_post)

#         return redirect('whatsapp')

class UserLoginView(LoginView):
    model = User
    form_class = LoginForm
    template_name = 'registration/login.html'


