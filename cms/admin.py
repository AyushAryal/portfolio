from django.contrib import admin
from .models import Skill, Social, Cv
from django.utils.html import format_html

admin.site.register(Skill)
admin.site.register(Social)

@admin.register(Cv)
class CvAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at', 'pdf_preview')
    readonly_fields = ('pdf_preview',)

    def pdf_preview(self, obj):
        if obj.pdf:
            return format_html(
                '<iframe src="/pdf_preview/{}" width="700" height="1000" style="border: none;"></iframe>',
                obj.pdf.name,
            )
        return "No PDF available"
    
    pdf_preview.short_description = "PDF Preview"

admin.site.site_header = "Ayush"
