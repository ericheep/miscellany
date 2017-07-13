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
    image = models.ImageField(upload_to='images')
    title = models.CharField(max_length=200, unique=True)

    image_type = models.CharField(max_length=1)

    def add(self):
        self.save()

    def __str__(self):
        return self.title


class Work(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True, editable=False)
    created_date = models.DateField()
    text = models.TextField(blank=True)
    abstract = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    images = models.ManyToManyField(Image, blank=True)

    featured = models.BooleanField(default=True)

    pdf = models.FileField(upload_to='pdfs', blank=True)
    vimeo = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    github = models.URLField(blank=True)

    # later at a artify thing to make it grayscale maybe, some sorta image script
    # would be cool
    thumbnail = models.ImageField(upload_to='thumbnails', blank=True)

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
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    work = models.ForeignKey(Work, blank=True)
    other = models.CharField(max_length=200, blank=True)

    collaborators = models.ManyToManyField(Collaborator)
    venue = models.ForeignKey(Venue)
    title = models.CharField(max_length=200)
    date = models.DateTimeField()

    def add(self):
        self.save()

    def __str__(self):
        return '%s, %s @ %s' % (self.date, self.work, self.venue)
