from django.core.exceptions import ValidationError
from django.db import models
from django.template.defaultfilters import slugify


class Audio(models.Model):
    title = models.CharField(max_length=200, null=True)
    text = models.TextField(blank=True)
    audio = models.FileField(upload_to='audio', blank=True)

    def __str__(self):
        return self.title or f'Audio #{self.pk}'


class Tag(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True, editable=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    title = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class Work(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(null=True, blank=True, editable=False)
    abstract = models.TextField(max_length=200)
    text = models.TextField(blank=True)
    body = models.TextField(
        blank=True,
        help_text='New-style page in Markdown with {image: title}, {audio: title}, '
                  '{vimeo: id} and {youtube: id} lines. When filled in, it replaces the old layout.',
    )
    created_date = models.DateField('start date')
    end_date = models.DateField(
        null=True, blank=True,
        help_text='Optional. Leave empty for a single date; fill in for a range like 2019–2022.')
    ongoing = models.BooleanField(
        default=False,
        help_text='Still in progress: shows as "2025–present" and sorts to the top of the works page.')
    tags = models.ManyToManyField(Tag, blank=True)
    images = models.ManyToManyField(Image, blank=True)
    mainImage = models.ImageField(upload_to='images', blank=True)

    featured = models.BooleanField(default=True)

    archive = models.FileField(upload_to='archive', blank=True)
    pdf = models.FileField(upload_to='pdfs', blank=True)
    vimeo = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    github = models.URLField(blank=True)

    audio = models.ManyToManyField(Audio, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        if self.mainImage:
            from .thumbnails import make_thumbnails, thumbs_current
            try:
                if not thumbs_current(self.mainImage.path):
                    make_thumbnails(self.mainImage.path)
            except Exception:
                pass  # the grid falls back to the original image

    def __str__(self):
        return self.title

    def clean(self):
        if self.ongoing and self.end_date:
            raise ValidationError({'end_date': 'An ongoing work has no end date. Clear one of the two.'})
        if self.end_date and self.created_date and self.end_date < self.created_date:
            raise ValidationError({'end_date': 'The end date is before the start date.'})

    def year_range(self):
        """Years only, for the works grid: 2022, 2019–2022 or 2025–present."""
        start = self.created_date.year
        if self.ongoing:
            return f'{start}–present'
        if self.end_date and self.end_date.year != start:
            return f'{start}–{self.end_date.year}'
        return str(start)

    def date_display(self):
        """For a work's own page: 'Mar, 2022' for a single date, otherwise the year range."""
        if self.ongoing or (self.end_date and self.end_date.year != self.created_date.year):
            return self.year_range()
        return self.created_date.strftime('%b, %Y')


class Venue(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Collaborator(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date = models.DateTimeField()
    work = models.ManyToManyField(Work, blank=True)
    other = models.CharField(max_length=200, blank=True)

    def __str__(self):
        if not self.pk:
            return self.title
        works = ', '.join(w.title for w in self.work.all()) or self.other or self.title
        return f'{self.date:%Y-%m-%d}, {works} @ {self.venue}'
