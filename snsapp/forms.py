from django import forms
from .models import Post
from django.contrib.auth.forms import AuthenticationForm
from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=254)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)


class LoginForm(AuthenticationForm):
    """ログインフォーム"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'tag']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'search-bar-input', 'placeholder': 'コメントを書く'}),
        }