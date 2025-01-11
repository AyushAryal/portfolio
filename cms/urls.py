from django.urls import path
from django.urls import re_path
from .views import pdf_preview_view

app_name = "cms"

urlpatterns = [
    # Other patterns
    re_path(r'^pdf_preview/(?P<pdf_path>.+)/$', pdf_preview_view, name='pdf_preview'),
]