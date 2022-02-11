from django.db import models


class Statistic(models.Model):
    path = models.CharField(max_length=500, blank=True, null=True)
    ip = models.CharField(max_length=100, blank=True, null=True)
    host = models.CharField(max_length=100, blank=True, null=True)
    referer = models.CharField(max_length=500, blank=True, null=True)
    user_agent = models.CharField(max_length=500, blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name_plural = ' لاگ ها'
        verbose_name = 'لاگ'

    def __str__(self):
        return "{0} {1}".format(self.create_time, self.path,)
