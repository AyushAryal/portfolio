from django.contrib import admin
from . import models

admin.site.register(models.Author)
admin.site.register(models.Tag)
admin.site.register(models.Article)
admin.site.site_header = "Ayush"
