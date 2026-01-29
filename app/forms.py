from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")#Which inputs appear on signup form

    def __init__(self, *args, **kwargs):#This is the constructor
        super().__init__(*args, **kwargs)#Calls Django’s original form setup
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-control"


class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs["class"] = "form-control"

from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complaint title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your complaint in detail'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 10:
            raise forms.ValidationError("Description must be at least 10 characters long.")
        return description


class StatusUpdateForm(forms.Form):
    status = forms.ChoiceField(
        choices=Complaint.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Add notes about this status change (optional)'
        }),
        required=False
    )

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if status not in dict(Complaint.STATUS_CHOICES):
            raise forms.ValidationError("Invalid status selected.")
        return status