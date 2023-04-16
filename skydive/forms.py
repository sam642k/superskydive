from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

from .models import Passenger, Applicant, Subscriber


class NewUserForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'search_input search_input_3'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'search_input search_input_3'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'search_input search_input_3'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'search_input search_input_3'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'search_input search_input_3'}))
    password_repeat = forms.CharField(label='Confirm Password',
                                      widget=forms.PasswordInput(attrs={'class': 'search_input search_input_3'}))
    phone_number = forms.CharField(required='False', widget=forms.NumberInput(attrs={'class': 'search_input '
                                                                                              'search_input_3'}))


class PassengerForm(forms.ModelForm):
    age = forms.IntegerField(validators=[MinValueValidator(18)])

    def _init_(self, *args, **kwargs):
        super(PassengerForm, self)._init_(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

    class Meta:
        model = Passenger
        fields = '__all__'


class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = ['first_name', 'last_name', 'phone', 'email', 'resume', 'cover_letter', 'comments']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone': 'Phone No.',
            'email': 'Email',
            'resume': 'Resume',
            'cover_letter': 'Cover Letter',
            'comments': 'Additional Comments'
        }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('email',)
