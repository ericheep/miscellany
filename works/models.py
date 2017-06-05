from django.db import models


class Work(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    discipline = models.CharField(max_length=50)
    created_date = models.DateTimeField()

    def add(self):
        self.save()

    def __str__(self):
        return self.title
