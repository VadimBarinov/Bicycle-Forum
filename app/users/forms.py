from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm,SetPasswordForm
from django.contrib.auth import get_user_model


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'Логин'
                               }))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'Пароль',
                                   'type': 'password'
                               }))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'Логин'
                               }))
    password1 = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'Пароль',
                                   'type': 'password'
                               }))
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'Повтор пароля',
                                   'type': 'password'
                               }))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'email': forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'E-mail'
                               }),
            'first_name': forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'Имя'
                               }),
            'last_name': forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'Фамилия'
                               }),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует')
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин',
                               disabled=True,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                               }))
    email = forms.CharField(label='E-mail',
                            disabled=True,
                            widget=forms.TextInput(attrs={
                               'class': 'form-input my-border form-control',
                            }))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                               }),
            'last_name': forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                               }),
        }


class UserPassworChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'Старый пароль',
                                   'type': 'password'
                               })
        )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'Новый пароль',
                                   'type': 'password'
                               })
        )
    new_password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'Повтор пароля',
                                   'type': 'password'
                               })
        )


class UserPasswordResetForm(PasswordResetForm):
    email = forms.CharField(label='E-mail',
                            widget=forms.TextInput(attrs={
                                'class': 'form-input my-border form-control',
                                'placeholder': 'E-mail'
                            }))

    class Meta:
        model = get_user_model()
        fields = ['email',]


class UserPasswordResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'Новый пароль',
                                   'type': 'password'
                               })
        )
    new_password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.TextInput(attrs={
                                   'class': 'form-input my-border form-control',
                                   'placeholder': 'Повтор пароля',
                                   'type': 'password'
                               })
        )

    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2',]
