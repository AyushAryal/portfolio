from django.db import models
from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.utils.html import format_html


class Social(models.Model):
    name = models.CharField(max_length=25, unique=True)
    url = models.URLField()

    def __str__(self):
        return str(self.name)

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = ColorField(default="#000000")

    def __str__(self):
        return str(self.name)

class Cv(models.Model):
    class Meta:
        verbose_name = "CV"  # Singular name
        verbose_name_plural = "CV"  # Plural name
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)
    
    def save(self, *args, **kwargs):
        if not self.pk and Cv.objects.exists():
            raise ValidationError("You can only have one instance of the Cv model.")
        super().save(*args, **kwargs)

    def pdf_preview(self):
        if self.pdf:
            return format_html('<embed src="{}" width="300" height="400" type="application/pdf">', self.pdf.url)
        return "No PDF uploaded"

    pdf_preview.short_description = "PDF Preview"