from django import forms
from .models import User

# creating Userform structure
class UserForm(forms.ModelForm):
    # For user registration form we are user User class as referance.
    password         = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','phone_no',]
    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get('password')
        confirm_passwod = cleaned_data.get('confirm_password')
        
        if password != confirm_passwod:
            raise forms.ValidationError("password doesn't match")