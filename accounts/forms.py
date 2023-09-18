from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Şifre giriniz',
        # 'class' : 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Şifreyi onaylayınız'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email','password']

    def __init__(self,*args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ad Giriniz'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Soyad Giriniz'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Telefon No Girininiz'
        self.fields['email'].widget.attrs['placeholder'] = 'E-posta Giriniz'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
