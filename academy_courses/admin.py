from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_per_page = 20
    

@admin.register(models.Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Slider)
class SliderAdmin(admin.ModelAdmin):
    list_per_page = 20


@admin.register(models.Urls)
class UrlsAdmin(admin.ModelAdmin):
    list_per_page = 20    


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    list_per_page = 20