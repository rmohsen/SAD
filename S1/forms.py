from django import forms
from material import *


class NameForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField(label="Email Address")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm password")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    identity_code = forms.IntegerField()
    type = forms.ChoiceField(choices=(('S', 'Student'), ('M', 'Manager'), ('O', 'Employee')))

    layout = Layout('username', 'email',
                    Row('password', 'password_confirm'),
                    Fieldset('Personal details',
                             Row('first_name', 'last_name')
                             , 'identity_code'
                             , 'type'))


class SignInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    layout = Layout('username', 'password')


class phase_type_form(forms.Form):
    name = forms.CharField()
    next_phase_type_acc = forms.IntegerField()  # next_phase_id
    next_phase_type_rej = forms.IntegerField()
    need_attachment = forms.BooleanField()
    need_transaction = forms.BooleanField()


class main_form(forms.Form):
    name = forms.CharField()
    data = forms.TextInput()
    attachment = forms.FileField()
    transaction = forms.IntegerField()


class phase_form(forms.Form):
    name = forms.CharField()
    phase_id = forms.IntegerField()


class process_form(forms.Form):
    name = forms.CharField()
    process_id = forms.IntegerField()


class process_type_form(forms.Form):
    name = forms.CharField()
    first_phase_type_id = forms.IntegerField()
