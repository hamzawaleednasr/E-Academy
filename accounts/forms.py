from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext as _

attrs = {'class': 'form-control'}



class UserLoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)


    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs=attrs)
    )    
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(attrs=attrs)
    )




class RegisterUserForm(UserCreationForm):
    
    first_name = forms.CharField(
        label=_('First Name'),
        widget=forms.TextInput(attrs=attrs)
    )  
    last_name = forms.CharField(
        label=_('Last Name'),
        widget=forms.TextInput(attrs=attrs)
    ) 

    username = forms.CharField(
        label=_('Username'),
        widget=forms.TextInput(attrs=attrs)
    )    
    email = forms.CharField(
        label=_('Email'),
        widget=forms.TextInput(attrs=attrs)
    ) 
    password1 = forms.CharField(
        label=_('Password'),
        strip=False,
        widget=forms.PasswordInput(attrs=attrs)
    )  
    password2 = forms.CharField(
        label=_('Password Confirmation'),
        strip=False,
        widget=forms.PasswordInput(attrs=attrs)
    )   
    is_staff = forms.BooleanField(
        label=_("Are you admin? "),
        required=False
    )
    
    # ADD THESE
    # I haven't worked out how to make them pretty, or how to include
    # the choices for the status, but I figure you can do that
    profile_image = forms.ImageField()

    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'last_name', 'username', 'email', 'is_staff',)

    field_order = ['first_name', 'last_name', 'username', 'profile_image', 'email', 'password1', 'password2', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_staff'].widget.attrs.update({
            'id': 'searchCheckbox'
        })


class ProfileForm(UserChangeForm):
    password = None
    class Meta():
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs=attrs),
            'last_name': forms.TextInput(attrs=attrs),
            'email': forms.EmailInput(attrs=attrs),
        }
