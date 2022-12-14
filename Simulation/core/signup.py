from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic import CreateView
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.models import Group

class SignUpForm(UserCreationForm):
    #email = forms.EmailField(required=False)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    group = forms.ModelChoiceField(queryset=Group.objects.all())

    def uniqueemailvalidator(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise ValidationError('User with this Email already exists.')

    def __init__(self, *args, **kwargs):
        #super().__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.fields['group'].required = True
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        # If one field gets autocompleted but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'
        #self.fields['email'].validators.append(self.uniqueemailvalidator)
    
    def clean_password2(self):
        password1 = "password"
        return password1

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'group','first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup.html'
    # def get_success_url(self):
    #     return reverse('home')


    def form_valid(self, form):
        user = form.save()
        group = Group.objects.get(name= form.cleaned_data['group']) 
        group.user_set.add(user)

        login(self.request, user)
        # feed = Feed.objects.create(user=user, post=welcome_post)

        return redirect('whatsapp')