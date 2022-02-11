from django.db import models


class SiteSettings(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان سایت')
    address = models.CharField(max_length=250, verbose_name='آدرس')
    phone = models.CharField(max_length=50, verbose_name='تلفن')
    mobile = models.CharField(max_length=50, verbose_name='تلفن همراه')
    email = models.EmailField(max_length=50, verbose_name='ایمیل')
    about_us = models.TextField(verbose_name='درباره ما', null=True, blank=True)
    copy_right = models.TextField(verbose_name='متن کپی رایت', null=True, blank=True)
    logo_image = models.ImageField(upload_to='upload/images/images', default='upload/images/no-img.jpg', null=True, blank=True, verbose_name='تصویر لوگو')
    whatsapp = models.CharField(max_length=150, verbose_name=' آدرس واتساپ', null=True, blank=True)
    instagram = models.CharField(max_length=150, verbose_name=' آدرس اینستاگرام', null=True, blank=True)
    telegram = models.CharField(max_length=150, verbose_name=' آدرس تلگرام', null=True, blank=True)
    twitter = models.CharField(max_length=150, verbose_name=' آدرس توييتر', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'تنظيمات سايت'
        verbose_name = 'تنظيمات'

    def __str__(self):
        return self.title
