from django.db import models


class Photo(models.Model):
    image = models.ImageField('Label', upload_to='static/media/')