from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _



class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name=_('User'), on_delete=models.CASCADE)
    profile_image = models.ImageField(verbose_name=_('Profile photo'), null=True, default='academy_courses/static/profile.jpg')
    courses = models.JSONField(verbose_name=_('Your Courses'), null=True)

    def __str__(self):
        return self.user.username