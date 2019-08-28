from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label = "Istifadeci Adi")
    password = forms.CharField(label = "Shifre", widget = forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(max_length= 50, label = "Istifadeci adi")
    password = forms.CharField(max_length=20, label = "Shifre", widget = forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label = "Shifre tekrari", widget = forms.PasswordInput)
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("yarragmi ye")
        else:
            values = {
                "username" : username,
                "password" : password,
            }
            return values
            