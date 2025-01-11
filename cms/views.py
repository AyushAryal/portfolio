from django.shortcuts import render

from django.http import FileResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from django.urls import path
from . import models

@xframe_options_exempt
def pdf_preview_view(request, pdf_path):
    file_path = f"media/{pdf_path}"
    return FileResponse(open(file_path, "rb"), content_type="application/pdf")
