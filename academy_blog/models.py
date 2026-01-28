from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import gettext as _
# Create your models here.

class Category(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=50)

    def __str__(self):
        return self.title


class Article(models.Model):
    cover_image = models.ImageField(verbose_name=_('Cover image'))
    category = models.ForeignKey(Category, verbose_name=_('Category'), on_delete=models.PROTECT)
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    subject = HTMLField(verbose_name=_('Subject'), max_length=10000)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)

    def __str__(self):
        return self.title