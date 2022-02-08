from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import User

class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(attrs={'class': 'form-input'})
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}))

class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-input'})
        self.fields['password2'] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input'}), help_text=None, label="Password Confirmation")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'image']

        widgets = {
            'username': forms.TextInput(attrs={'class': "form-input"}),
            'email': forms.TextInput(attrs={'class': "form-input"}),
            'image': forms.FileInput(attrs={'class': "form-input"}),
        }

        help_texts = {
            'username': None,
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'image', )
        help_texts = {'username': None}
        labels = {'image': None}
        initialValues = {'image': None}

        widgets = {
            'username': forms.TextInput(attrs={'class': "form-input"}),
            'email': forms.TextInput(attrs={'class': "form-input"}),
            'image': forms.FileInput(attrs={'class': "form-input"}),
        }

class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({'class': 'form-input'})

class UserPasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs.update({'class': 'form-input'})
        self.fields["new_password2"].widget.attrs.update({'class': 'form-input'})

class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-input'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-input'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-input'})