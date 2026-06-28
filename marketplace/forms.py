from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import FreelanceGig, Profile, Order


class GigForm(forms.ModelForm):
    class Meta:
        model = FreelanceGig
        fields = ['title', 'description', 'price', 'delivery_time_days', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., I will design a modern logo'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 5, 'placeholder': 'Describe your service in detail...'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'e.g., 50.00', 'step': '0.01', 'min': '1'}),
            'delivery_time_days': forms.NumberInput(attrs={'class': 'form-input', 'min': '1', 'placeholder': 'e.g., 3'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'your@email.com'}))
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-input'}), label='I want to join as')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Choose a username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Create a password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-input', 'placeholder': 'Confirm your password'})


class OrderSubmissionForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['submission_text', 'submission_file']
        widgets = {
            'submission_text': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 5,
                'placeholder': 'Provide notes, descriptions, or URLs to your completed work (e.g., Google Drive link)...'
            }),
            'submission_file': forms.ClearableFileInput(attrs={'class': 'form-input'}),
        }
