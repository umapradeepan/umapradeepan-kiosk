from django.db import models

class ResultItem (models.Model):
    content = models.TextField()
    parkcode = models.TextField()
