from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Article)
class ArticleAdminModel(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Category)
class CategoryAdminModel(admin.ModelAdmin):
    list_per_page = 20    