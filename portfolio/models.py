from django.db import models
from django.template.defaultfilters import slugify, truncatechars


class Tag(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True, editable=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='img')
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    def add(self):
        self.save()

    def __str__(self):
        return self.title


class Work(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True, editable=False)
    created_date = models.DateField()

    featured = models.BooleanField(default=True)
    # pdf = models.FileField(blank=True)
    github = models.URLField(blank=True)
    text = models.TextField(blank=True)
    images = models.ManyToManyField(Image, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def short_text(self):
        return truncatechars(self.text, 50)

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


class Collaborator(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Performance(models.Model):
    work = models.ForeignKey(Work, blank=True)
    other = models.CharField(max_length=200, blank=True)

    collaborators = models.ManyToManyField(Collaborator)
    venue = models.ForeignKey(Venue)
    event = models.CharField(max_length=200)
    date = models.DateTimeField()

    def add(self):
        self.save()

    def __str__(self):
        return '%s, %s @ %s' % (self.date, self.work, self.venue)
