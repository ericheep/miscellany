from django.db import models
from django.contrib.postgres.fields import ArrayField


class Work(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    discipline = models.CharField(max_length=50)
    created_date = models.DateField()
    tags = ArrayField(
        models.CharField(max_length=20, null=True),
        null=True
    )

    def add(self):
        self.save()

    def __str__(self):
        return self.title


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()

    def add(self):
        self.save()

    def __str__(self):
        return self.name


class Performance(models.Model):
    work = models.ForeignKey(Work)
    venue = models.ForeignKey(Venue)
    date = models.DateTimeField()
    location = models.CharField(max_length=50)

    def add(self):
        self.save()

    def __str__(self):
        return '%s %s' % (self.venue, self.date)


class Image(models.Model):
    work = models.ForeignKey(Work, null=True)
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)

    def add(self):
        self.save()

    def __str__(self):
        return self.name
