from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Şifre giriniz',
        # 'class' : 'form-control',
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Şifreyi onaylayınız'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Ad Giriniz'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Soyad Giriniz'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Telefon No Girininiz'
        self.fields['email'].widget.attrs['placeholder'] = 'E-posta Giriniz'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'Parola eşleşmiyor'
            )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            Account.objects.get(email=email)
            raise forms.ValidationError('Bu e-posta adresi zaten bir hesapla ilişkilendirilmiş.')
        except Account.DoesNotExist:
            return email
