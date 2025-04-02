from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


@admin.register(DailyPrice)
class DailyPriceAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in DailyPrice._meta.fields]
admin.site.register(Index)