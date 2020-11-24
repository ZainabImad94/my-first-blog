from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, validate_email


def clean_user_info(value):
    if not value.isalpha():
        raise ValidationError('Only characters are allowed !')
    else:
        return value


alpha = RegexValidator(r'^[0-9a-zA-Z_\-.]*$', 'Only number, character & (-,_) are allowed !')


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        max_length=100,
        widget=forms.TextInput(
            attrs={'placeholder': 'example@example.com'}
        ),
        required=True,
        validators=[validate_email]
    )
    first_name = forms.CharField(
        label='First Name',
        max_length=40,
        min_length=3,
        required=True,
        widget=forms.TextInput(
            attrs={'autofocus': 'True'}
        ),
        validators=[clean_user_info]
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=40,
        min_length=4,
        required=True,
        validators=[clean_user_info]
    )
    username = forms.CharField(
        label='Username',
        max_length=150,
        min_length=4,
        required=True,
        validators=[alpha]
    )
    password1 = forms.CharField(
        label='Password',
        max_length=50,
        min_length=8,
        required=True,
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Password Confirmation',
        max_length=50,
        min_length=8,
        required=True,
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email is already in use! Try another email.')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal container-fluid justify-content-center'
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Fieldset("Sign Up",
                     'first_name',
                     'last_name',
                     'username',
                     'email',
                     'password1',
                     'password2',
                     Submit('Submit', 'Create New Account', css_class="btn-primary text-canter")
                     )
        )
