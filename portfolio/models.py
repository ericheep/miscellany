from django.db import models
from django.template.defaultfilters import slugify


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
#    thumbnail = models.ImageField(upload_to='thumbs', editable=False)

#    def save(self, *args, **kwargs):
#        """
#        Make and save the thumbnail for the photo here.
#        """
#        super(Image, self).save(*args, **kwargs)
#        if not self.make_thumbnail():
#            raise Exception('Could not create thumbnail - is the file type valid?')
#
#
#    def make_thumbnail(self):
#        """
#        Create and save the thumbnail for the photo (simple resize with PIL).
#        """
#        fh = storage.open(self.photo.name, 'r')
#        try:
#            image = Image.open(fh)
#        except:
#            return False
#
#        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)
#        fh.close()
#
#        # Path to save to, name, and extension
#        thumb_name, thumb_extension = os.path.splitext(self.photo.name)
#        thumb_extension = thumb_extension.lower()
#
#        thumb_filename = thumb_name + '_thumb' + thumb_extension
#
#        if thumb_extension in ['.jpg', '.jpeg']:
#            FTYPE = 'JPEG'
#        elif thumb_extension == '.gif':
#            FTYPE = 'GIF'
#        elif thumb_extension == '.png':
#            FTYPE = 'PNG'
#        else:
#            return False    # Unrecognized file type
#
#        # Save thumbnail to in-memory file as StringIO
#        temp_thumb = StringIO()
#        image.save(temp_thumb, FTYPE)
#        temp_thumb.seek(0)
#
#        # Load a ContentFile into the thumbnail field so it gets saved
#        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=True)
#        temp_thumb.close()
#
#        return True

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
    title = models.CharField(max_length=200)
    venue = models.ForeignKey(Venue)
    date = models.DateTimeField()
    work = models.ManyToManyField(Work, blank=True)
    other = models.CharField(max_length=200, blank=True)

    def add(self):
        self.save()

    def __str__(self):
        return '%s, %s @ %s' % (self.date, self.work, self.venue)


class Audio(models.Model):
    title = models.CharField(max_length=200)
    upload = models.FileField(upload_to='audio')
