from django import forms
from .models import FarmerProfile, WellDetails
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
 
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ['location', 'farm_size', 'soil_type', 'water_source']
        widgets = {
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'farm_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'soil_type': forms.Select(attrs={'class': 'form-control'}),
            'water_source': forms.Select(attrs={'class': 'form-control'}),
        }

class WellDetailsForm(forms.ModelForm):
    class Meta:
        model = WellDetails
        fields = ['diameter', 'depth', 'water_level', 'last_measured']
        widgets = {
            'diameter': forms.NumberInput(attrs={'class': 'form-control'}),
            'depth': forms.NumberInput(attrs={'class': 'form-control'}),
            'water_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'last_measured': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

 
class VoiceQueryForm(forms.Form):
    query = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ask your agriculture question...'
        }),
        label=''
    )