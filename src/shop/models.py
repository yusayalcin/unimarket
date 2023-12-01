from django.db import models
from django.db.models.fields import related
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from mysite.settings import EMAIL_HOST_USER

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

import random
import string

from django.core.mail import send_mail


def generate_code(length):
    result_str = "".join(random.choice(string.ascii_letters) for i in range(length))

    return result_str


def send_activation_email(code, email):
    if email[email.index("@") + 1 :] in [
        "ppk.elte.hu",
        "btk.elte.hu",
        "inf.elte.hu",
        "ajk.elte.hu",
        "tok.elte.hu",
        "ttk.elte.hu",
        "tatk.elte.hu",
        "barczi.elte.hu",
        "student.elte.hu",
    ]:
        subject = "Welcome to Unimarket"
        message = f"Hope you will enjoy our platform!\nActivate your account: http://localhost:8080/profile/activation/?code={code}"
        send_mail(subject, message, EMAIL_HOST_USER, [email], fail_silently=False)
        print("OK!")


class Category(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=20)
    is_published = models.BooleanField(verbose_name=_("is_published"), default=True)
    image = models.FileField(verbose_name=_("image"), upload_to="image/cat/")

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.title


class Goods(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=20)
    is_published = models.BooleanField(verbose_name=_("is_published"), default=True)
    is_recommend = models.BooleanField(verbose_name=_("is_recommend"), default=False)
    is_top = models.BooleanField(verbose_name=_("is_top"), default=False)
    is_active = models.BooleanField(verbose_name=_("is_active"), default=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, verbose_name=_("category")
    )
    price = models.FloatField(verbose_name=_("price"))
    image = models.FileField(verbose_name=_("image"), upload_to="image/goods/")
    text = models.TextField(verbose_name=_("text"))
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("product")
        verbose_name_plural = _("products")
        ordering = ("category", "title")

    def __str__(self):
        return self.title


class Carousel(models.Model):
    title = models.CharField(verbose_name=_("title"), max_length=100)
    text = models.CharField(verbose_name=_("text"), max_length=200)
    image = models.FileField(verbose_name=_("image"), upload_to="image/carousel/")

    class Meta:
        verbose_name = _("slide")
        verbose_name_plural = _("slides")

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField()
    facebook = models.TextField()
    phone = models.TextField()
    code = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            code = generate_code(255)
            Profile.objects.create(user=instance, code=code)
            if not instance.is_superuser:
                send_activation_email(code, instance.username)
        else:
            instance.profile.save()
            



    @receiver(pre_save, sender=User)
    def pre_save_user(sender, instance, **kwargs):
        if instance.id is None and not instance.is_superuser:
            instance.is_active = False
