from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=150, verbose_name='نام')
    email = models.EmailField(max_length=200, verbose_name='ايميل')
    mobile = models.CharField(max_length=11, blank=True, verbose_name='موبايل')
    message = models.TextField(verbose_name='متن پيام')
    date = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال پيام')


    class Meta:
        verbose_name_plural = 'پيام ها'
        verbose_name = 'پيام'

    def __str__(self):
        return "{} : {}".format(self.email, self.message[0:50])

   