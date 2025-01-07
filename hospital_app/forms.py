from django import forms
from .models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    birthdate = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2024)))
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'role', 'birthdate') 

    password = forms.CharField(widget=forms.PasswordInput)

class AvailabilityForm(forms.Form):
    AVAILABILITY_CHOICES = [('Available', 'Available'), ('Not Available', 'Not Available')]
    availability = forms.ChoiceField(choices=AVAILABILITY_CHOICES, widget=forms.RadioSelect)
