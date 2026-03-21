from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].empty_label = 'Выберите автора'

    class Meta:
        model = Post
        fields = ['author','title', 'text', 'category']
        label = {
            'author': 'Автор',
            'title': 'Заголовок',
            'text': 'Содержание',
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'cols': 38}),
        }


