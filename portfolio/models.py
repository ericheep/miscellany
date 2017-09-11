from django.db import models
from django.template.defaultfilters import slugify


class Audio(models.Model):
    title = models.CharField(max_length=200, null=True)
    text = models.TextField(blank=True)
    audio = models.FileField(upload_to='audio', blank=True)

    def __str__(self):
        return self.title

    def add(self):
        self.save()


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

    def add(self):
        self.save()

    def __str__(self):
        return self.title


class Work(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True, editable=False)
    abstract = models.TextField(max_length=200)
    text = models.TextField(blank=True)
    created_date = models.DateField()
    tags = models.ManyToManyField(Tag, blank=True)
    images = models.ManyToManyField(Image, blank=True)

    featured = models.BooleanField(default=True)

    archive = models.FileField(upload_to='archive', blank=True)
    pdf = models.FileField(upload_to='pdfs', blank=True)
    vimeo = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    github = models.URLField(blank=True)

    audio = models.ManyToManyField(Audio, blank=True)

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
    title = models.CharField(max_length=200)
    venue = models.ForeignKey(Venue)
    date = models.DateTimeField()
    work = models.ManyToManyField(Work, blank=True)
    other = models.CharField(max_length=200, blank=True)

    def add(self):
        self.save()

    def __str__(self):
        return '%s, %s @ %s' % (self.date, self.work, self.venue)
