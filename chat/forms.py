from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import ChatRoom

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'placeholder': ("Username"),"class":"required", "title":"Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."})   
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': ("Password"),'data-toggle':"popover","class":"required", "title":"""
        Your password can’t be too similar to your other personal information.\nYour password must contain at least 8 characters.\nYour password can’t be a commonly used password.\nYour password can’t be entirely numeric."""})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': ("Password again"),"class":"required", "title":"Enter the same password as before, for verification."})    
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Your username already exists. Try to choose another one.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Your e-mail already exists. Try to choose another one.")
        return email


class Log_in_form(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(Log_in_form, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
                 'placeholder': 'Username',
                 "class":"required"})
        self.fields['password'].widget.attrs.update({
                 'placeholder': 'Password',
                 "class":"required"})
        

class ChatRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['name']