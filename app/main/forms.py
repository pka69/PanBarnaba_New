from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    user = forms.CharField(label='Nick:', max_length=64)
    password = forms.CharField(label='hasło:', max_length=64, widget=forms.PasswordInput)


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="podaj hasło")
    repeat_password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="Powtórz hasło")
    
    class Meta:
        model = User
        fields = ['username', 'password', 'repeat_password', 'email']  # 'first_name', 'last_name', 

    def clean(self):
        super(CreateUserForm, self).clean
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']
        username = self.cleaned_data['username']
        if password != repeat_password:
            raise ValidationError('Hasła sie różnią od siebie')
        if User.objects.filter(username=username):
            raise ValidationError('Podany użytkownik {} już istnieje'.format(username))
    
    def save(self, commit=True):
        # Skopiowane z oryginalnej wersji
        if self.errors:
            raise ValueError(
                "konto %s nie może być %s. Taki uzytkownik już istnieje" % (
                    self.instance._meta.object_name,
                    'utworzone' if self.instance._state.adding else 'zmienione',
                )
            )
        try:
            return User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                # first_name=self.cleaned_data['first_name'],
                # last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email'],
            )
        except KeyError:
                return User.objects.create_user(
                username=self.cleaned_data['username'],
                password=self.cleaned_data['password'],
                # first_name=self.cleaned_data['first_name'],
                # last_name=self.cleaned_data['last_name'],
                # email=self.cleaned_data['email'],
            )

class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="podaj nowe hasło")
    repeat_password = forms.CharField(max_length=64, widget=forms.PasswordInput, label="Powtórz nowe hasło")

    def clean(self):
        super(PasswordChangeForm, self).clean()
        new_password = self.cleaned_data['new_password']
        repeat_password = self.cleaned_data['repeat_password']
        if new_password != repeat_password:
            raise ValidationError('Hasła sie różnią od siebie')