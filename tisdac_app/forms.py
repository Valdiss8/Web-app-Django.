from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Visitor, Feedback
from datetime import date, datetime, timedelta


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = '__all__'

        labels = {
            'name': 'Your name',
            'phone': 'Your phone',
            'email': 'Your email',
        }

class EventForm(forms.Form):
    name = forms.CharField(label='Your name',  max_length=30, min_length=2)
    phone = forms.CharField(label='Your phone', required=False,  max_length=15)
    email = forms.EmailField(label='You email')


#class FedbackForm(forms.ModelForm):
#    class Meta:
#        model = Feedback
#        fields = '__all__'
#        exclude = ('date',)
#        labels = {
#            'name': 'Your name',
#            'phone': 'Your phone',
#            'email': 'Your email',

#        }

class FeedbackForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=30, min_length=2, required=True)
    phone = forms.CharField(label='Your phone', max_length=20, required=False)
    email = forms.EmailField(label='Your email', required=True)
    feedback = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40})) #по умолчанию 10 и 40



class ServiceForm(forms.Form):
    name = forms.CharField(label='Name', max_length=20, min_length=2, error_messages={
        #'max_length': 'Слишком много символов',
        #'min_length': 'Слишком мало символов',
        #'required': 'Укажите хотя бы один символ'

    })

    email = forms.EmailField()
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

#class LoginUserForm(AuthenticationForm):
 #   username =
  #  password =
   # class Meta:
   #     model = User
    #    fields = ('username', 'password1', )