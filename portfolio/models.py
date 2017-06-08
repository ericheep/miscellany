from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.template.defaultfilters import slugify


class Work(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True, editable=False)

    text = models.TextField()
    discipline = models.CharField(max_length=50)
    created_date = models.DateField()

    tags = ArrayField(
        models.CharField(max_length=20),
        null=True, blank=True
    )

    def add(self):
        self.save()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Work, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def add(self):
        self.save()

    def __str__(self):
        return self.name


class Performance(models.Model):
    work = models.ForeignKey(Work)
    venue = models.ForeignKey(Venue)
    date = models.DateField()

    def add(self):
        self.save()

    def __str__(self):
        return '%s, %s @ %s' % (self.date, self.work, self.venue)


class Image(models.Model):
    work = models.ForeignKey(Work, null=True)
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)

    def add(self):
        self.save()

    def __str__(self):
        return self.name
