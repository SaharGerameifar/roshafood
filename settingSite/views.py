from django.shortcuts import render
from .models import SiteSettings
# Create your views here.


def aboutus(request, *args, **kwargs):
    site_setting = SiteSettings.objects.first()
    context = {
        'site_setting': site_setting,
    }

    return render(request, 'about.html', context)