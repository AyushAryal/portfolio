from django.db import models
from django.utils import timezone
from colorfield.fields import ColorField
from ckeditor_uploader.fields import RichTextUploadingField

THUMBNAIL_DIR = "article_thumbnails"
PROFILE_PICTURE_DIR = "profile_picture"

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()
    profile_picture = models.ImageField(blank=True, null=True, upload_to=PROFILE_PICTURE_DIR)

    def __str__(self):
        return self.name


class Tag(models.Model):
    tag = models.CharField(max_length=100)
    color = ColorField(default="#000000")
    description = models.TextField()

    def __str__(self):
        return self.tag


class Article(models.Model):
    title = models.CharField(max_length=500)
    pub_date = models.DateTimeField("Publication date",default=timezone.now)
    content = RichTextUploadingField()
    authors = models.ManyToManyField(Author)
    tags = models.ManyToManyField(Tag)
    thumbnail = models.ImageField(blank=True, null=True, upload_to=THUMBNAIL_DIR)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title
