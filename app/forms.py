from django import forms
from django.forms.models import ModelForm
from django.forms import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .models import *
from datetime import datetime 
class registerform(UserCreationForm):
    email = forms.EmailField(required=True)
  
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
class postform(ModelForm):
    class Meta:
        model=post
        fields=['title','content','image']
class commentform(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['comment_content','image']
        widgets = {
            'comment_content': forms.Textarea(attrs={'rows': 2}),}       

class ProfileForm(forms.ModelForm):
    RELATIONSHIP_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        # Add more choices as needed
    ]

    status = forms.ChoiceField(choices=RELATIONSHIP_STATUS_CHOICES)
    def clean_date_of_birth_data(self):
        date_of_birth=self.cleaned_data['date_of_birth']
        currunt_year=datetime.now().year
        if date_of_birth.year >currunt_year-11:
            raise ValidationError(
                'the age is not suitable for our website'
            )
        return date_of_birth
    class Meta:
        model = profile
        fields = ['profile_pic', 'bio', 'date_of_birth', 'status', 'lives_in']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }