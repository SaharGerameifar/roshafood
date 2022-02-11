from . import models

def log(request):
    print("path", request.path)
    statistic = models.Statistic()

    if request.path:
        statistic.path = request.path

    if 'User-Agent' in request.headers:
        statistic.user_agent = request.headers['User-Agent']

    if 'Host' in request.headers:
        statistic.host = request.headers['Host']

    if 'Referer' in request.headers:
        statistic.referer = request.headers['Referer']

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        statistic.ip = x_forwarded_for.split(',')[0]
    else:
        statistic.ip = request.META.get('REMOTE_ADDR')

    statistic.save()
