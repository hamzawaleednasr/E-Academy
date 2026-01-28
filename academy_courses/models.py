from django.db import models
from django.conf.global_settings import AUTH_USER_MODEL
from django.utils.translation import gettext as _

# Create your models here.

ACTIVE_CHOICES = (
    ("", "Select status"),
    ("active", "Active"),
    (" ", "Inactive"),
)


SOCIAL_MEDIA_ICONS = [
    ("", "Select an icon"),
    ("fa-facebook", "Facebook"),
    ("fa-twitter", "Twitter"),
    ("fa-instagram", "Instagram"),
    ("fa-linkedin", "LinkedIn"),
    ("fa-youtube", "YouTube"),
    ("fa-pinterest", "Pinterest"),
    ("fa-tumblr", "Tumblr"),
    ("fa-flickr", "Flickr"),
    ("fa-github", "GitHub"),
    ("fa-bitbucket", "Bitbucket"),
    ("fa-gitlab", "GitLab"),
    ("fa-stack-overflow", "Stack Overflow"),
    ("fa-medium", "Medium"),
    ("fa-reddit", "Reddit"),
    ("fa-whatsapp", "WhatsApp"),
    ("fa-skype", "Skype"),
]



class Course(models.Model):
    name = models.CharField(verbose_name=_('Course title'), max_length=50)
    description = models.TextField(verbose_name=_('Course description'), max_length=5000)
    price = models.FloatField(verbose_name=_('Price'))
    hour = models.IntegerField(verbose_name=_('Course hours'))
    min = models.IntegerField(verbose_name=_('Course minutes'))
    image = models.ImageField(verbose_name=_('Cover image'))
    created_at = models.DateTimeField(verbose_name=_('Created at') ,auto_now_add=True)    
    updated_at = models.DateTimeField(verbose_name=_('Updated at') ,auto_now=True)

    def __str__(self):
        return self.name
    

class Video(models.Model):
    title = models.CharField(verbose_name=_('Video title'), max_length=100)
    desc = models.TextField(max_length=1000)
    video = models.FileField(verbose_name=_('Video'))
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    course = models.ForeignKey(Course, verbose_name=_('Course'), on_delete=models.CASCADE)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)

    def __str__(self):
        return self.title


class Opinion(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=50)
    career = models.CharField(verbose_name=_('career'), max_length=100)
    image = models.ImageField(verbose_name=_('Personal photo'))
    message = models.TextField(verbose_name=_('Message'), max_length=500)

    def __str__(self):
        return self.name


class Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.CASCADE)
    video = models.ForeignKey(Video, verbose_name=_('Video'), on_delete=models.CASCADE)
    message = models.TextField(verbose_name=_('Comment'))
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)


class Slider(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=100)
    image = models.ImageField(verbose_name=_('Slider image'))
    is_active = models.CharField(
        verbose_name=_('Is active'),
        max_length=50,
        choices=ACTIVE_CHOICES,
        default='Select status',
    )


class Urls(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=30, default="My Urls")
    icon = models.CharField(
        verbose_name=_('Icon'),
        default='Select an icon',
        choices=SOCIAL_MEDIA_ICONS,
        max_length=100
    )
    url = models.URLField(verbose_name=_('Url'))

    def __str__(self):
        return self.title
    

class TransactionStatus(models.IntegerChoices):
    Pending = 0, _('Pending')
    Completed = 1, _('Completed')


class Transaction(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name=_('User'), on_delete=models.PROTECT)
    course = models.ForeignKey(Course, verbose_name=_('Course'), on_delete=models.PROTECT)
    status = models.IntegerField(
        choices=TransactionStatus.choices, default=TransactionStatus.Pending, verbose_name=_('Status')
    )
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)


class Order(models.Model):
    transaction = models.OneToOneField(Transaction, verbose_name=_('Transaction'), on_delete=models.PROTECT, null=True)
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)    

    def __str__(self):
        return str(self.id)
    
    class Meta:
            verbose_name = _('Order')
            verbose_name_plural = _('Orders')
    

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, verbose_name=_('Order'), on_delete=models.PROTECT)    
    course = models.ForeignKey(Course, verbose_name=_('Course'), on_delete=models.PROTECT)
    price = models.FloatField(verbose_name=_('Price'))
    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)