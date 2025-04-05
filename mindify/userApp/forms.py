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

class ProfileEditForm(forms.Form):
    profile_picture = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'class': 'form-control form-floating',
        'id': 'profilePicture'
    }))
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control form-floating',
        'placeholder': 'First Name',
        'id': 'profileFirstName'
    }))
    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control form-floating',
        'placeholder': 'Last Name',
        'id': 'profileLastName'
    }))
    gender = forms.ChoiceField(
        required=False,
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-control form-floating',
            'id': 'profileGender'
        }))