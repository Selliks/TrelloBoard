from django import forms
from django.contrib.auth.models import User
from .models import Status, Task, Unit, Role


class TaskForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=False
    )

    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        empty_label="Оберіть статус",
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'unit', 'deadline', 'status']
        widgets = {
            'unit': forms.CheckboxSelectMultiple(),
        }


class TaskEditForm(forms.ModelForm):
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'unit', 'deadline', 'status']
        widgets = {
            'unit': forms.CheckboxSelectMultiple(),
        }


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label='Username',
        error_messages={'required': 'This field is required'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password',
        error_messages={'required': 'This field is required'}
    )


class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(max_length=32, required=True, label="First Name")
    last_name = forms.CharField(max_length=64, required=True, label="Last Name")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")

        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
