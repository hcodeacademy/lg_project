
from django import forms
from account.models import UserAccount


class UserForm(forms.ModelForm):
    class Meta:
        model= UserAccount
        fields = ('first_name','last_name','email','gender','state_of_origin','local_origin',
                  'Occupation','marital_status','father_name', 'mother_name','contact_address',
                  'date_of_birth','place_of_birth','passport')
  