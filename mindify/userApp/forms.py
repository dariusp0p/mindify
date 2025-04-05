from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-floating',
        'placeholder': 'Email',
        'id': 'loginEmail'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-floating',
        'placeholder': 'Password',
        'id': 'loginPassword'
    }))

class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control form-floating',
        'placeholder': 'Username',
        'id': 'signupUsername'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control form-floating',
        'placeholder': 'Email',
        'id': 'signupEmail'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control form-floating',
        'placeholder': 'Password',
        'id': 'signupPassword'
    }))