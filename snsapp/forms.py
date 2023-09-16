from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'tag']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'search-bar-input', 'placeholder': 'コメントを書く'}),
        }