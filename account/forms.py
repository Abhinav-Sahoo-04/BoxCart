from django import forms
from .models import Account,UserProfile

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter your password',
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm your password',
    }))
    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone_number','password']
    
    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter your first name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter your last name'
        self.fields['email'].widget.attrs['placeholder']='Enter your email'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter your phone number'

    def clean(self):
        cleaned_data=super(RegistrationForm,self).clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')
        if password!=confirm_password:
            raise forms.ValidationError(
                "Password does not match !"
            )

class UserForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=['first_name','last_name','phone_number']


class ProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False,error_messages={"Invalid":("Image file only !")},widget=forms.FileInput)
    class Meta:
        model=UserProfile
        fields=['address_line_1','address_line_2','city','state','country','profile_picture']