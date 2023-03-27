from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

TYPE_CHOICES = (
    ('Student', 'Student'),
    ('Teacher', 'Teacher'),
)


class ExtendSignup(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='Student')
    coin_choices = models.TextField(null=True)

    def __str__(self):
        return self.type


class CoinDetails(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=20)
    price = models.FloatField(null=True, max_length=200)
    percent_change_1h = models.FloatField(null=True, max_length=200)
    percent_change_24h = models.FloatField(null=True, max_length=200)
    percent_change_7d = models.FloatField(null=True, max_length=200)
    volume_24h = models.FloatField(null=True, max_length=200)
    market_cap = models.FloatField(null=True, max_length=200)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to="profile_picture/", default="profile_picture/None/blank-profile.png")


class NewsDetails(models.Model):
    url = models.URLField(max_length=250)
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=1000)
    image_url = models.URLField(max_length=300)
    published_at = models.DateTimeField()
    source_domain = models.URLField(max_length=50)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    create_user_profile: Signals to create user profile data
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    save_user_profile: Signals to save user profile data
    :rtype: object
    :param sender:
    :param instance:
    :param kwargs:
    """
    instance.profile.save()
