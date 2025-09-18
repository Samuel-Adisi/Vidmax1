from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms 
from.models import Video,Videos

class Register(UserCreationForm):

    class Meta:
        model=User
        fields=('username','password1')

class CreateForm(forms.ModelForm):
    class Meta:
        model=Videos
        fields=['title','video_file','thumbnail_image',]
        exclude=('userComments','duration')
      






    