from django.contrib import admin
from .models import ReadTime

# Register your models here.
@admin.register(ReadTime)
class ReadTimeAdmin(admin.ModelAdmin):
    list_display = ('read_time','content_object')