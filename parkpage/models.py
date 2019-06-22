from django.db import models

class AlertItem (models.Model):
    title = models.TextField()
    desc = models.TextField()
    url = models.TextField()
class CenterItem (models.Model):
    name = models.TextField()
    desc = models.TextField()
    dir = models.TextField()
class LessonItem (models.Model):
    title = models.TextField()
    q2 = models.TextField()
    url = models.TextField()
