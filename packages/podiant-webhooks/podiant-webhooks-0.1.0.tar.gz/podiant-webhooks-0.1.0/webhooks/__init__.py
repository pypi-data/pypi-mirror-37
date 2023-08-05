__version__ = '0.1.0'


def send(name, data):
    from .models import Webhook

    for webhook in Webhook.objects.filter(name=name):
        webhook.send(data)
