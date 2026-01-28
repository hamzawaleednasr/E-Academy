from django import forms
from .models import Course, Video, Transaction
from tinymce.widgets import TinyMCE

field_attrs = {'class': 'form-control'}

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'description', 'price', 'hour', 'min', 'image']
        widgets = {
            'name': forms.TextInput(),
            'description': forms.Textarea(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'desc', 'video']
        widgets = {
            'title': forms.TextInput(attrs=field_attrs),
            'desc': forms.Textarea(attrs=field_attrs),
            'course': forms.Select(attrs=field_attrs),
        }
