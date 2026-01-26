from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from .models import Complaint

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

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = "__all__"
        exclude = []  # You can add any fields you want to exclude here if needed
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "user": forms.Select(attrs={"class": "form-control"}),  # For user field, assuming it's a ForeignKey
            "created_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),  # Customize the input type
        }