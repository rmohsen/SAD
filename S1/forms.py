from django import forms
from material import *


class NameForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    type = forms.ChoiceField(choices=(('S', 'Student'), ('M', 'Manager'), ('O', 'Employee')))
    receive_news = forms.BooleanField(required=False, label='I want to receive news and special offers')
    agree_toc = forms.BooleanField(required=True, label='I agree with the Terms and Conditions')

    layout = Layout('username', 'email',
                    Row('password', 'password_confirm'),
                    Fieldset('Personal details',
                             Row('first_name', 'last_name'),
                             'type', 'receive_news', 'agree_toc'))


class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    layout = Layout('username', 'password')


class phase_type_form(forms.Form):
    name = forms.CharField()
    phase_type_id = forms.IntegerField()
    next_phase_type_acc = forms.IntegerField()  # next_phase_id
    next_phase_type_rej = forms.IntegerField()

class process_form(forms.Form):
    name = forms.CharField()


class process_type_form(forms.Form):
    name = forms.CharField()
    first_phase_type_id = forms.IntegerField()
