from django import forms
from .models import Post
from django.contrib.auth.forms import AuthenticationForm

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