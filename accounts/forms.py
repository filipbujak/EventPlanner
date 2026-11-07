from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adres e-mail")
    first_name = forms.CharField(max_length=150, required=False, label="Imię")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = "Od 3 do 30 znaków: litery, cyfry i @/./+/-/_"
        # self.fields["username"].help_text = ""  # <- odkomentuj, żeby ukryć całkowicie

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Konto z takim adresem e-mail już istnieje.")
        return email