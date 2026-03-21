from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User, Group
from django.contrib import messages

from django.contrib.auth import get_user_model


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super() .__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['email'].label = 'Адрес электронной почты'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтверждение пароля'
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


    email = forms.EmailField()


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class MyCustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = ''
        self.fields['email'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)

        return user

class CustomUserCreationForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.groups.add(Group.objects.get(name='common'))
        return user