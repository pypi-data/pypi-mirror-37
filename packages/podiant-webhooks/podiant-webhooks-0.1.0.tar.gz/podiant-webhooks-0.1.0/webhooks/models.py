from django.db import models
import requests


class Webhook(models.Model):
    name = models.SlugField(max_length=100, unique=True)
    url = models.URLField(max_length=511)

    def __str__(self):
        return self.name.replace('-', ' ').replace('_', ' ').capitalize()

    def send(self, data):
        requests.post(self.url, json=data)
