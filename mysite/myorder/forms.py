from django import forms
from django.contrib.auth.models import User
from .models import Profilis


class UserUpdateForm(forms.ModelForm):
    """Vartotojo duomenų atnaujinimo klasė"""
    email = forms. EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfilisUpdateForm(forms.ModelForm):
    """Profilio nuotraukos pridėjimas"""
    class Meta:
        model = Profilis
        fields = ['nuotrauka']

class DateInput(forms.DateInput):
    """ši data keliauja i užsakymo atlikimo lauką"""
    input_type = "date"
