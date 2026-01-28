from django import forms
from .models import Article
from tinymce.widgets import TinyMCE

field_attrs = {'class': 'form-control'}

class ArticleForm(forms.ModelForm):
    subject = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Article
        fields = ['cover_image', 'category', 'title', 'subject']
        widgets = {
            'category': forms.Select(attrs=field_attrs),
            'title': forms.TextInput(attrs=field_attrs),
        }