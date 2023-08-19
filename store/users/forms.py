from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from users.models import User


class UserLoginForm(AuthenticationForm):  # 4.8, 4.10  создаем красивые формы для регистрации (указываем где в login.html брать логин и пароль)
    username = forms.CharField(widget=forms.TextInput(attrs={  # текст в форме TextInput не скрывается в PasswordInput скрывается
        'class': "form-control py-4", 'placeholder': "Введите имя пользователя"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите пароль"}))

    class Meta:  # принимает доп параметры которые отвечают за то с какой моделью будет работать данная форма и какими полями
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):  # 4.11
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите имя"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите фамилию"}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите имя пользователя"}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите адрес эл. почты"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Введите пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': "form-control py-4", 'placeholder': "Подтвердите пароль"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):  # 4.12
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4"}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': "custom-file-input"}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control py-4", 'readonly': True}))  # readonly неизменяемые поля в профиле
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': "form-control py-4", 'readonly': True}))  # readonly неизменяемые поля в профиле

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email')
