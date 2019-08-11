from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from contacts.models import Contact


class ContactForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3)
    class Meta:
        model = Contact
        fields = ('first_name', 'last_name', 'email', 'message')
