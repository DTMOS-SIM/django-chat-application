from django.contrib.auth.models import User
from django import forms
from .models import *


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class LoginForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class UserProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Others')]
        model = AppUser
        fields = ('dob', 'gender')
        widgets = {
            'gender': forms.Select(choices=CHOICES),
            'dob': forms.DateInput(attrs={'type': 'date'})
        }


class ImageMediaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ImageMediaForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-sm'

    class Meta:
        model = Images
        fields = ('name', 'description', 'user')


class ChatRoomForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChatRoomForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Rooms
        fields = ('name', 'description', 'user')


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chats
        fields = ('message', 'user', 'room')
